# Description: Custom Jinja2 filter for Netapp ontap specific tasks

class FilterModule(object):

    
    def filters(self):
        return {
            'auth_pw':self.auth_rest,
            'auth_cert':self.auth_cert,
            'auth_rest':self.auth_rest
        }
    
    def auth_rest(self,hostname,username,password="",cert_base="",use_cert=False,https=True,validate_certs=False):
        if not cert_base and not password:
            raise ValueError("Either password or cert_base must be provided")
        if use_cert:
            key_filepath = f"{cert_base}.key"
            cert_filepath = f"{cert_base}.crt"
            return self.auth_cert(hostname,key_filepath,cert_filepath,https,validate_certs)
        else:
            return self.auth_pw(hostname,username,password,https,validate_certs)

    def auth_pw(self,hostname,username,password,https=True,validate_certs=False):
        # return a dictionary with the authentication headers
        return {
            "hostname":hostname,
            "username":username,
            "password":password,
            "https":https,
            "validate_certs":validate_certs
        }

    def auth_cert(self,hostname,key_filepath,cert_filepath,https=True,validate_certs=False):
        # return a dictionary with the authentication headers
        return {
            "hostname":hostname,
            "key_filepath":key_filepath,
            "cert_filepath":cert_filepath,
            "https":https,
            "validate_certs":validate_certs
        }
