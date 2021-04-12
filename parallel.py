import multiprocessing
import time

def heavy(n, i, proc):
    for x in range(1, n):
        for y in range(1, n):
            x**y
    print(f"Вычисление № {i} процессор {proc}")


def sequential(calc, proc):
    print(f"Запускаем поток № {proc}")
    for i in range(calc):    
        heavy(500, i, proc)
    print(f"{calc} циклов вычислений закончены. Процессор № {proc}")
    

def pooled(core=None):
    # вычисляем количество ядер процессора
    n_proc = multiprocessing.cpu_count() if core is None else core
    # вычисляем количество операций на процесс 
    calc =  int(80 / n_proc) if 80 % n_proc == 0 else int(80 // n_proc + 1)
    # создаем список инициализации функции 
    # sequential(calc, proc) для каждого процесса
    init = map(lambda x: (calc, x), range(n_proc))
    with multiprocessing.Pool() as pool:
       pool.starmap(sequential, init)
    
    print (calc, n_proc, core)
    return (calc, n_proc, core)

if __name__ == "__main__":
    start = time.time()
    # в целях эксперемента, укажем количество
    # ядер больше чем есть на самом деле
    calc, n_proc, n = pooled(20)
    end = time.time()
    text = '' if n is None else 'задано ' 
    print(f"Всего {text}{n_proc} ядер процессора")
    print(f"На каждом ядре произведено {calc} циклов вычислений")
    print(f"Итого {n_proc*calc} циклов за: ", end - start)