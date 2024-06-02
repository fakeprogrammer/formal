import ddmp

def main():
    process_P = ddmp.Process(['P0', 'P1', 'P2'],
                        [
                            ['a', 'P0', 'P1'],
                            ['a', 'P0', 'P1'],
                            ['a', 'P0', 'P2'],
                        ])

    process_Q = ddmp.Process(['Q0', 'Q1', 'Q2', 'Q3'],
                        [
                            ['a', 'Q0', 'Q1'],
                            ['a', 'Q0', 'Q2'],
                            ['a', 'Q0', 'Q3'],
                        ])

    p: ddmp.Process = ddmp.concurrent_composition(process_P, process_Q, ['a'])

if __name__== "__main__":
    main()
