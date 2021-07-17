import kociemba

def get_solution(str_total):
    '''
    ->str_solve
    红:Up 绿:Front 白:Left 黄:Right 橙:Down 蓝:Back
    '''
    str_total = str_total.replace('R', 'U')
    str_total = str_total.replace('G', 'F')
    str_total = str_total.replace('W', 'L')
    str_total = str_total.replace('Y', 'R')
    str_total = str_total.replace('O', 'D')
    str_solve = kociemba.solve(str_total)

    list_test = ['U', 'R', 'F', 'D', 'L', 'B']

    for i, a in enumerate(list_test):
        str_solve = str_solve.replace(a, a+'1')
        str_solve = str_solve.replace(a+"1'", a+'2')
        str_solve = str_solve.replace(a+'12', a+'3')
    str_solve = ''.join(str_solve.split())

    return str_solve