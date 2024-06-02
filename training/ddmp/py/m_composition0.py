import ddmp

def main():
    process_P = ddmp.Process(['P0', 'P1', 'P2', 'P3', 'P4'],
                        [
                            ['a', 'P0', 'P1'],
                            ['b', 'P0', 'P2'],
                            ['c', 'P0', 'P3'],
                            ['e', 'P0', 'P4'],
                        ])

    process_Q = ddmp.Process(['Q0', 'Q1', 'Q2', 'Q3'],
                        [
                            ['a', 'Q0', 'Q1'],
                            ['c', 'Q0', 'Q2'],
                            ['d', 'Q0', 'Q3'],
                        ])

    p: ddmp.Process = ddmp.concurrent_composition(process_P, process_Q, ['a', 'b'])

if __name__== "__main__":
    main()
