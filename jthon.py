#!/usr/bin/python3

def calc( expr, env=None ):
    t = expr[0]
    if t == "quote":
        return expr[1]
    elif t == "let":
        for bindings in expr[2:]:
            e = {}
            for k, v in bindings.items():
                e[k] = calc( v, env=env )
            env = (e, env)
        return calc( expr[1], env=env )
    elif t == "letrec":
        e = {}
        env = ( e, env )
        for k, v in expr[2].items():
            e[k] = calc( v, env=env )
        return calc( expr[1], env=env )
    elif t == "ref":
        name = expr[1]
        while not( env is None ):
            ( e, env ) = env
            if name in e:
                return e[ name ]
        raise Exception( "Unbound variable" )
    elif t == "if":
        test = calc( expr[1], env=env )
        return calc( expr[ 2 if test else 3 ], env=env )
    elif t == "lambda":
        return ("closure", expr, env)
    elif t == "apply":
        fn = calc( expr[1], env=env )
        args = [ calc( e, env=env ) for e in expr[2:] ]
        # The fn value should be a closure.
        try:
            ( closure_kw, lambda_form, captured_env ) = fn
            assert closure_kw == "closure"
            ( lambda_kw, params, body ) = lambda_form
            assert lambda_kw == "lambda"
        except:
            raise Exception( "Closure needed: {}".format( fn ) )
        e = {}
        for i in range( 0, len( params ) ):
            e[ params[i] ] = args[i]
        return calc( body, env=( e, captured_env ) )
    elif t == "+":
        return calc( expr[1], env=env ) + calc( expr[2], env=env ) 
    elif t == "-":
        return calc( expr[1], env=env ) - calc( expr[2], env=env ) 
    elif t == "<=":
        return calc( expr[1], env=env ) <= calc( expr[2], env=env ) 
    else:
        raise Exception( "Unhandled expression: {}".format( t ) )

NFIB_CODE = (
    ["letrec",
        ["apply", ["ref", "nfib"], ["quote", 15] ],
        {
            "nfib" : ["lambda", ["n"], 
                ["if", 
                    ["<=", ["ref", "n"], ["quote", 1]],
                    ["quote",1],
                    ["+", ["quote", 1], 
                        ["+",
                            ["apply", ["ref", "nfib"], ["-", ["ref", "n"], ["quote", 1]]],
                            ["apply", ["ref", "nfib"], ["-", ["ref", "n"], ["quote", 2]]]
                        ]
                    ]
                ]
            ]
        }
    ]
)


TEST_CODE = (
    ["let",
        ["apply", ["ref", "test"], ["quote", 88] ],
        {
            "test": ["lambda", ["x"], ["+", ["quote", 1], ["ref", "x"]]]
        }
    ]
)

if __name__ == "__main__":
    print( calc( ["let", ["+", ["ref","x"], ["quote", 1] ], { "x": [ "quote", 99 ] } ] ) )  
    print( calc( ["if", ["<=", ["quote",3], ["quote", 1] ], ["quote", "a"], ["quote", "b"] ] ) )
    print( calc( TEST_CODE ) )  
    print( calc( NFIB_CODE ) )
