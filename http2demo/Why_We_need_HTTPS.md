### HTTPS的设计由来

最初client和Server使用HTTP进行通信，通信内容是明文传输的，可能会遭遇中间人劫持。

```javascript
Client ----PlainText----> Server
Server ----PlainText----> Client
```

```javascript
Client ----PlainText----> Server
Client ----PlainText----> Hacker ----FakedPlainText-----> Server
Server ----PlainText----> Hacker ----FakedPlainText-----> Client
```

为了解决上面这个问题，有学者提出了对通信内容进行加密，比如对称加密AES。

```
Client ----AESEncryptData----> Server
```

即使攻击者截取了加密的数据，没有密钥的情况下是无法解密的。但Server端如何解密呢，我所能想到的方式有两种：

1. Client发送密钥（Key）给Server
2. Server主动向Client索要Key

```javascript
Client ----Key----> Server
Client ----AESEncryptData----> Server
```

先来看第二种方式存在的现实问题，一台Server可能同时与多台Client通信，在通信之前Server无法获取Client的位置，所以无法索要Key，即使能够提前知道Client的位置，仍需要Client发送密钥给Server。

第一种方式存在的问题是如果发送密钥的请求被劫持了，后续的加密通信便没有意义。Server无法区分请求是中间人还是Client发送过来的，这是**身份验证**的问题。为了解决这个问题，有人建议使用公钥加密算法进行加密（RSA）。

```javascript
EncryptKey = Encrypt(Key, PublicKey) //On Client
Client ----EncryptKey----> Server
Key = Decrypt(EncryptKey, PrivateKey) //On Server
Server ----Ok,I get the key---->Client
Client ----AESEncryptData---->Server (Use the EncryptKey to Decrypt Data)
```

在这个模型中，存在以下几个问题：

1. 客户端的PublicKey是如何获取的
2. 服务端的私钥是如何获取的

解决该问题有两种算法，一是RSA算法，另外一种是DH算法。

RSA算法，Server端生成一对钥匙，并保留私钥，对所有客户端发布公钥，这种方法似乎是可行的，实际却会遭遇下面两种情况。

1. 攻击者生成一对钥匙，并对外发布，劫持通讯
2. 客户端存储每个Server的证书，无法实现，客户端数量过多且不确定

忽略第二种情况，第一种情况本质是劫持的问题。即服务端向客户端发送的公钥被中间人劫持了，中间人将自己的公钥发送给客户端，客户端收到后使用假公钥进行通信，中间人使用自己的私钥解密并用劫持的真公钥对信息加密，再发送给服务端。那么该如何保护公钥呢，继续使用RSA算法加密保护吗？这就仿佛绕进了一个“先有鸡还是先有蛋”的问题了。

先来看DH算法的实现原理，DH算法原理非常简单，如下所示。

```
Client 
Private Number: a

Shared Number: g & p

Server
Private Number: b

Calcuated New number:
A = g^a mod p
B = g^b mod p

Exchange Number A and B
Client:  Key = g^a x B  ===> Key = g^a x g^b mod p
Server:  Key = g^b x A  ===> key = g^b x g^a mod p
```

整个通讯过程中，g、p、A、B是明文已知的，但攻击者无法计算出Key的值，所以可以确保公钥的安全，但仍能遭遇中间人攻击。为了解决这个问题，引入了签名（RSA、Md5、SHA等）机制。

```
小明与小红写信通讯，为了防止劫持，每封信上都会带上各自的专属签名。
```

问题又来了，签名是可以被伪造的，我该信任什么？为了解决签名的伪造问题，引入了第三方权威机构，由第三方机构来保证Server的身份。具体的实现如下：

```
1. 服务器提供公钥，域名等信息给权威机构
2. 权威机构根据公钥和服务器、域名等信息，使用私钥进行签名制作成证书
3. 服务器与客户端通信时，将数字证书发送给客户端
4. 客户端会根据浏览器(多数情况下是浏览器)内置的证书通过单向散列算法进行身份校验
5. 身份校验成功，取出服务器的公钥，用于加密会话密钥
```

#### 数字证书和数字签名

签名是为了防止消息被篡改(完整性)，签名过程如下

```
1. Message Digest= Hash(Message)
2. Signature = encrypt(Message Digest, sender's private key)
3. Send message and Signature to Receiver
```

签名校验过程如下

```
1. Message Digest1 = Decrypt(Signature, recevier's public key)
2. Message Digest2 = Hash(Message)
3. If compare(Digest1, Digest2)
```

证书是为了防止消息被调包，证书制作过程如下

```
1. Encrypt = RSAEncrypt(digest, domain and server info, server's publickey, privatekey) 
2. Send Encrypt
```

### SSL/TLS CipherSuite

一个CipherSuite由4个算法组成：

1. 认证算法（authentication），防止身份伪造
2. 加密算法（encryption），防止消息被窃取
3. 消息认证码（message authentication code），防止消息被篡改
4. 密钥认证（key exchange），防止密钥被替换

带关联的认证数据加密（Authenticated Encryption with Associated Data）



由于对称加密(symmetric encryption)需要传输密钥，所以非对称加密(asymmetric encryption)用于保护密钥的交换。



**前向安全**或**前向保密**（英语：Forward Secrecy，缩写：FS），有时也被称为**完美前向安全**[[1\]](https://zh.wikipedia.org/wiki/%E5%89%8D%E5%90%91%E5%AE%89%E5%85%A8%E6%80%A7#cite_note-1)（英语：Perfect Forward Secrecy，缩写：PFS），是[密码学](https://zh.wikipedia.org/wiki/%E5%AF%86%E7%A0%81%E5%AD%A6)中通讯协议的安全属性，指的是长期使用的主[密钥](https://zh.wikipedia.org/wiki/%E5%AF%86%E9%92%A5)泄漏不会导致过去的[会话密钥](https://zh.wikipedia.org/wiki/%E6%9C%83%E8%A9%B1%E5%AF%86%E9%91%B0)泄漏。



### 参考

1. https://www.wst.space/ssl-part-2-diffie-hellman-key-exchange/
2. https://tls13.ulfheim.net/
3. [数字签名是什么](http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html)
4. [也许，这样理解HTTPS更容易](http://blog.jobbole.com/110354/)