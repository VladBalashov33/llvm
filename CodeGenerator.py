from llvmlite import ir, binding

class CodeGen():
    def __init__(self):
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()
        self._config_llvm()
        self._create_execution_engine()
        self._declare_print_function()

    def _config_llvm(self):
        # Config
        global base_func
        self.module = ir.Module(name=__file__)
        self.module.triple = self.binding.get_default_triple()

        func_type = ir.FunctionType(ir.VoidType(), [], False)
        base_func = ir.Function(self.module, func_type, name="main")
        block = base_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

    def _create_execution_engine(self):
        # Engine
        target = self.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = binding.parse_assembly("")
        engine = binding.create_mcjit_compiler(backing_mod, target_machine)
        self.engine = engine

    def _declare_print_function(self):
        # Printf
        voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        self.printf = printf

    def _compile_ir(self):
        # Compile
        self.builder.ret_void()

        pmb = self.binding.create_pass_manager_builder()
        pm = self.binding.create_module_pass_manager()
        pm.add_constant_merge_pass()
        pm.add_dead_arg_elimination_pass()
        pm.add_function_attrs_pass()
        pm.add_dead_code_elimination_pass()
        pm.add_gvn_pass()
        pm.add_instruction_combining_pass()
        pmb.populate(pm)

        llvm_ir = str(self.module)
        mod = self.binding.parse_assembly(llvm_ir)
        x = pm.run(mod)


        mod.verify()
        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()

        self.module=mod
        return mod

    def create_ir(self):
        self._compile_ir()

    def save_ir(self, filename):
        S=str(self.module).replace(r'local_unnamed_addr #0','')
        S = S.replace(r'local_unnamed_addr #1', '')
        S=S.replace('source_filename = "<string>"','')
        S = S.replace('x86_64-pc-win32', 'x86_64-pc-linux-gnu')
        with open(filename, 'w') as output_file:
            output_file.write(S)

# -----------------------------------------------------------------------------------------------------------------------------