from __future__ import absolute_import, print_function

import re

from autogen import rebuild
rebuild()

with open('cypari2/auto_gen.pxi') as f:
    auto_gen = f.read()
with open('cypari2/gen.pyx') as f:
    gen = f.read()
with open('cypari2/auto_instance.pxi') as f:
    auto_instance = f.read()
with open('cypari2/pari_instance.pyx') as f:
    instance = f.read()

re_func = re.compile('^    def (?P<name>[^\s()]*)\(', re.MULTILINE)

gen_func = set(re_func.findall(gen))
auto_gen_func = set(re_func.findall(auto_gen))
common_func = gen_func.intersection(auto_gen_func)

print('{} functions in gen'.format(len(gen_func)))
print('{} functions in auto_gen'.format(len(auto_gen_func)))
print('{} functons in common:\n   - {}'.format(len(common_func), '\n   - '.join(sorted(common_func))))
