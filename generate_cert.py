from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, Encoding, NoEncryption, PrivateFormat, PublicFormat
from cryptography.hazmat.backends import default_backend
import datetime
import os

def generate_certificates(cert_path='cert.pem', key_path='key.pem', password=None):
    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # 创建证书主题和颁发者名称
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'localhost'),
    ])

    # 创建证书
    certificate = x509.CertificateBuilder().subject_name(
        name
    ).issuer_name(
        name
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # 证书有效期：1年
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u'localhost')]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())

    # 写入私钥到文件
    with open(key_path, 'wb') as key_file:
        if password:
            encryption_algorithm = BestAvailableEncryption(password.encode())
        else:
            encryption_algorithm = NoEncryption()
        key_file.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=encryption_algorithm,
        ))

    # 写入证书到文件
    with open(cert_path, 'wb') as cert_file:
        cert_file.write(certificate.public_bytes(Encoding.PEM))

if __name__ == '__main__':
    # 指定证书和密钥文件的存放路径
    cert_dir = 'certs'
    os.makedirs(cert_dir, exist_ok=True)
    generate_certificates(os.path.join(cert_dir, 'cert.pem'), os.path.join(cert_dir, 'key.pem'))
    print(f"证书和私钥已生成在 {cert_dir} 目录下")
