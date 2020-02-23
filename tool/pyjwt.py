import jwt
import time
bs = jwt.encode({'username':'wangyajun','exp':time.time() + 300},'123456',algorithm='HS256')
print(jwt.decode(bs,'123456',algorithms='HS256'))