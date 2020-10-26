from src.utils import Utils

cache = Utils.cache('VisitLancashire_scraped')
print(cache)
if cache == '1':
    print('Cache exists')
else:
    print('Cache not exists')