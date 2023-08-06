import rematch as re

regex = ".*!x{a+}.*"
document = "aaaaaa"

rgx = re.RegEx(regex)
it = rgx.findIter(document)

# for match in it:
#   print('\t'.join('!{}: {}'.format(v, match.span(v)) for v in match.variables())

count = 0

while it.hasNext():
  match = it.next()
  print('\t'.join('!{}: {}'.format(v, match.span(v)) for v in match.variables()))
  count += 1

print(count)