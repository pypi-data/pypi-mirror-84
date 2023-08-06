
# ContextM
##### *My package does this*

### Instillation
    python -m pip install contextM

### Usage
    import contextM
    
    class my_context_manager(contextM.ContextManager):
        def __init__(self, var):
            self.var = var
        def __enter__(self):
            print('Enter!')
            return self
        def __exit__(self, *args, **kwargs):
            print('Exit!')

### Features
    ContextManager class:
    * See Implementation Above