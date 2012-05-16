import os
import subprocess

KC = 'security'
SSL = 'openssl'

class KeychainManager(object):
    filename = None

    def __init__(self,name):
        self.name = name
        self.file()

    def create(self):
        os.system('%s create-keychain -p "" %s' % (KC,self.name))
        self.file()

    def delete(self):
        os.system('%s delete-keychain %s' % (KC,self.filename))

    def exists(self):
        return self.name in os.popen('%s list-keychains' % (KC,)).read()

    def export_identities(self,p12_file):
        os.system('%s export -k %s -t identities -f pkcs12 -P "" -o %s' % (KC,self.filename,p12_file))

    def file(self):
        if self.filename:
            return self.filename
        files = KeychainManager.keychain_files()
        for f in files:
            if self.name in f:
                self.filename = f
                continue    
        return self.filename

    #TODO: test
    def import_apple_cert(self,apple_cert_file):
        os.system('%s import %s -k %s' % (KC,apple_cert_file,self.filename))

    #TODO: test
    def import_rsa_cert(self,rsa_cert_file):
        os.system('%s import %s -P "" -k %s' % (KC,rsa_cert_file,self.filename))

    #TODO: test
    @classmethod
    def convert_p12_to_pem(cls,p12_file,pem_file):
        os.system('%s pkcs12 -passin pass: -nodes -in %s -out %s' % (SSL,p12_file,pem_file))

    #TODO: test
    @classmethod
    def generate_cert_request(cls,email,country,rsa_file,cert_file):
        os.system('%s req -new -key %s -out %s  -subj "/%s, CN=CERT_NAME, C=%s"' % (SSL,rsa_file,cert_file,email,country))

    #TODO: test
    @classmethod
    def generate_rsa_key(cls,rsa_file, keysize=2048):
        os.system('%s genrsa -out %s %s' % (SSL,rsa_file,keysize))

    @classmethod
    def keychain_files(cls):
        files = []
        results = os.popen('%s list-keychains' % (KC,)).read().split('\n')
        for f in results:
            files.append(f.strip().replace('"',''))
        return files
