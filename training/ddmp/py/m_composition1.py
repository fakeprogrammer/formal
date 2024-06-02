import ddmp

def main():
    process_P = ddmp.Process(['P0', 'P1', 'P2', 'P3'],
                        [
                            ['a', 'P0', 'P1'],
                            ['c', 'P1', 'P2'],
                            ['d', 'P2', 'P3'],
                        ])

    process_Q = ddmp.Process(['Q0', 'Q1', 'Q2', 'Q3', 'Q4'],
                        [
                            ['b', 'Q0', 'Q1'],
                            ['c', 'Q1', 'Q2'],
                            ['d', 'Q2', 'Q3'],
                            ['e', 'Q3', 'Q4'],
                        ])

    p: ddmp.Process = ddmp.concurrent_composition(process_P, process_Q, ['c', 'e'])

if __name__== "__main__":
    main()
