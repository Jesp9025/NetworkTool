#https://github.com/richardpenman/pywhois
#https://www.pythonforbeginners.com/dns/using-pywhois
import whois
w = whois.whois("google.com")
print(w)
#It may say there is an error and whois is not callable.. Ignore it.
