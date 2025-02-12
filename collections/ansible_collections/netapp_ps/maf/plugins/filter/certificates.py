# let's create a custom filter plugin to handle certificate manipulations

class FilterModule(object):

    '''
    custom jinja merge vars Filter
    '''
    
    def filters(self):
        return {
        'parse_pem_output':self.parse_pem_output,
        'get_expiry_date':self.get_expiry_date,
        }
    
    def parse_pem_output(self,input,indicator):

        # let's split the input by lines
        lines = input.split('\n')
        # let's find the index of the signing request, based on the indicator
        # the start index should have the work "BEGIN {indicatr}" 
        # the end index should have the word "END {indicator}"
        
        pem_index = lines.index(f'-----BEGIN {indicator}-----')
        pem_end_index = lines.index(f'-----END {indicator}-----')

        PEM = '\n'.join(lines[pem_index:pem_end_index+1])
        return PEM
                 
    def get_expiry_date(self,input,asString=False,output_format='%Y-%m-%d %H:%M:%S'):
        # get the expiry date from a PEM certificate
        # let's use the cryptography module to parse the certificate
        from cryptography import x509

        cert = x509.load_pem_x509_certificate(input.encode())
        expiry_date = cert.not_valid_after

        if asString:
            return expiry_date.strftime(output_format)

        return expiry_date