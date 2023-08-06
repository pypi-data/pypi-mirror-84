"""
TESTS:

From ``gen.__repr__``::

    sage: pari('vector(5,i,i)')
    [1, 2, 3, 4, 5]

From ``gen.__str__``::

    sage: print(pari('vector(5,i,i)'))
    [1, 2, 3, 4, 5]


From ``gen.__list__``. For polynomials, list() behaves as for ordinary Sage
polynomials::

    sage: pol = pari("x^3 + 5/3*x"); pol.list()
    [0, 5/3, 0, 1]

From ``gen.__add__`` and ``gen.__sub__``::

    sage: RR("2e20") + pari("1e20")
    3.00000000000000 E20
    sage: RR("2e20") - pari("1e20")
    1.00000000000000 E20

From ``gen._nf_get_pol``

    sage: K.<a> = NumberField(x^4 - 4*x^2 + 1)
    sage: pari(K).nf_get_pol()
    y^4 - 4*y^2 + 1

For relative number fields, this returns the relative
polynomial. However, beware that ``pari(L)`` returns an absolute
number field::

    sage: L.<b> = K.extension(x^2 - 5)
    sage: pari(L).nf_get_pol()        # Absolute
    y^8 - 28*y^6 + 208*y^4 - 408*y^2 + 36
    sage: L.pari_rnf().nf_get_pol()   # Relative
    x^2 - 5

TESTS::

    sage: x = polygen(QQ)
    sage: K.<a> = NumberField(x^4 - 4*x^2 + 1)
    sage: K.pari_nf().nf_get_pol()
    y^4 - 4*y^2 + 1
    sage: K.pari_bnf().nf_get_pol()
    y^4 - 4*y^2 + 1


    sage: K.<a> = NumberField(x^4 - 4*x^2 + 1)
    sage: pari(K).nf_get_diff()
    [12, 0, 0, 0; 0, 12, 8, 0; 0, 0, 4, 0; 0, 0, 0, 4]

    sage: K.<a> = NumberField(x^4 - 4*x^2 + 1)
    sage: s = K.pari_nf().nf_get_sign(); s
    [4, 0]
    sage: type(s); type(s[0])
    <... 'list'>
    <... 'int'>
    sage: CyclotomicField(15).pari_nf().nf_get_sign()
    [0, 4]

    sage: K.<a> = NumberField(x^4 - 4*x^2 + 1)
    sage: pari(K).nf_get_zk()
    [1, y, y^3 - 4*y, y^2 - 2]

    sage: K.<a> = QuadraticField(-65)
    sage: K.pari_bnf().bnf_get_no()
    8

    sage: K.<a> = QuadraticField(-65)
    sage: G = K.pari_bnf().bnf_get_gen(); G
    [[3, 2; 0, 1], [2, 1; 0, 1]]
    sage: [K.ideal(J) for J in G]
    [Fractional ideal (3, a + 2), Fractional ideal (2, a + 1)]

"""
