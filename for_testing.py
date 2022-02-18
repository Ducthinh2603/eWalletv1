from repositories import repositories_helper

content = {
  "merchantId": "e90518d0-612d-4a61-869e-40fccd51200f",
  "amount": 200,
  "extraData": "Cart1",
  "signature": "37a277f67c311572b73552b0c89d6410"
}
key = "e549e963-ef10-4e06-b703-21b75613f93b"
rs = repositories_helper.signature_generator(key, **content)
print(rs)