KC = 'security'
SSL = 'openssl'

class KeychainManager(object):
    self.file = None

    def __init__(self,name):
        self.name = name

    def create(self):
        return '%s create-keychain -p "" %s' % (KC,self.name)

    def delete(self):
        return '%s delete-keychain %s' % (KC,self.file)

    def exists(self):
        return False

    def export_identities(self,p12_file):
        return '%s export -k %s -t identities -f pkcs12 -P "" -o %s' % (KC,self.file,p12_file)

    def file(self):
        if self.file:
            return self.file
        files = KeychainManager.keychain_files()
        for f in files:
            if self.name is in f:
                self.file = f
                continue    
        return self.file

    def import_apple_cert(self,apple_cert_file):
        return '%s import %s -k %s' % (KC,apple_cert_file,self.file)

    def import_rsa_cert(self,rsa_cert_file):
        return '%s import %s -P "" -k %s' % (KC,rsa_cert_file,self.file)

    #class methods
    def convert_p12_to_pem(p12_file,pem_file):
        return '%s pkcs12 -passin pass: -nodes -in %s -out %s' % (SSL,p12_file,pem_file)

    def generate_cert_request(email,country,rsa_file,cert_file):
        return '%s req -new -key %s -out %s  -subj "/%s, CN=CERT_NAME, C=%s"' % (SSL,rsa_file,cert_file,email,country)

    def generate_rsa_key(rsa_file, keysize=2048):
        return '%s genrsa -out %s %s' % (SSL,rsa_file,keysize)

    #need to actually do the loop properly
    def keychain_files():
        files = []
        cmd = '%s list-keychains' % (KC,)
        results = []
        for f in results:
            files.append(f)
        return files
