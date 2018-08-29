from urllib.parse import urlparse

my_url = 'google.com/sdsf /sdf'
p = urlparse(my_url, 'http')
 
if p.netloc:
    netloc = p.netloc
    path = p.path
else:
    netloc = p.path
    path = ''
 
if not netloc.startswith('www.'):
    netloc = 'www.' + netloc
 
p = p._replace(netloc=netloc, path=path)
print(p.geturl())