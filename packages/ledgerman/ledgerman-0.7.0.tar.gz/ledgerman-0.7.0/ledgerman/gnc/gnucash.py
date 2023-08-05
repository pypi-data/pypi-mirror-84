import uuid
import gzip


class GNUCash:
    def header():
        return """<?xml version="1.0" encoding="utf-8" ?>
<gnc-v2
 xmlns:gnc="http://www.gnucash.org/XML/gnc"
 xmlns:act="http://www.gnucash.org/XML/act"
 xmlns:book="http://www.gnucash.org/XML/book"
 xmlns:cd="http://www.gnucash.org/XML/cd"
 xmlns:cmdty="http://www.gnucash.org/XML/cmdty"
 xmlns:price="http://www.gnucash.org/XML/price"
 xmlns:slot="http://www.gnucash.org/XML/slot"
 xmlns:split="http://www.gnucash.org/XML/split"
 xmlns:sx="http://www.gnucash.org/XML/sx"
 xmlns:trn="http://www.gnucash.org/XML/trn"
 xmlns:ts="http://www.gnucash.org/XML/ts"
 xmlns:fs="http://www.gnucash.org/XML/fs"
 xmlns:bgt="http://www.gnucash.org/XML/bgt"
 xmlns:recurrence="http://www.gnucash.org/XML/recurrence"
 xmlns:lot="http://www.gnucash.org/XML/lot"
 xmlns:addr="http://www.gnucash.org/XML/addr"
 xmlns:billterm="http://www.gnucash.org/XML/billterm"
 xmlns:bt-days="http://www.gnucash.org/XML/bt-days"
 xmlns:bt-prox="http://www.gnucash.org/XML/bt-prox"
 xmlns:cust="http://www.gnucash.org/XML/cust"
 xmlns:employee="http://www.gnucash.org/XML/employee"
 xmlns:entry="http://www.gnucash.org/XML/entry"
 xmlns:invoice="http://www.gnucash.org/XML/invoice"
 xmlns:job="http://www.gnucash.org/XML/job"
 xmlns:order="http://www.gnucash.org/XML/order"
 xmlns:owner="http://www.gnucash.org/XML/owner"
 xmlns:taxtable="http://www.gnucash.org/XML/taxtable"
 xmlns:tte="http://www.gnucash.org/XML/tte"
 xmlns:vendor="http://www.gnucash.org/XML/vendor">"""

    def empty(
        accountId=uuid.uuid4().hex,
        bookId=uuid.uuid4().hex,
    ):
        return GNUCash.header() + (
            """
<gnc:count-data cd:type="book">1</gnc:count-data>
<gnc:book version="2.0.0">
<book:id type="guid">"""
            + bookId
            + """</book:id>
<gnc:count-data cd:type="commodity">1</gnc:count-data>
<gnc:count-data cd:type="account">1</gnc:count-data>
<gnc:commodity version="2.0.0">
  <cmdty:space>template</cmdty:space>
  <cmdty:id>template</cmdty:id>
  <cmdty:name>template</cmdty:name>
  <cmdty:xcode>template</cmdty:xcode>
  <cmdty:fraction>1</cmdty:fraction>
</gnc:commodity>
<gnc:account version="2.0.0">
  <act:name>Root Account</act:name>
  <act:id type="guid">"""
            + accountId
            + """</act:id>
  <act:type>ROOT</act:type>
</gnc:account>
</gnc:book>
</gnc-v2>"""
        )

    def toFile(fileName, data):
        f = open(fileName, "wb")
        f.write(gzip.compress(bytes(data, "utf-8")))


# compressed_value = gzip.compress(bytes(empty(), "utf-8"))
# plain_string_again = gzip.decompress(compressed_value)

GNUCash.toFile("z.gnucash", GNUCash.empty())
