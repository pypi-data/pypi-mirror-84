from typing import Set, Type, Any, List, Dict, Optional

from antlr4 import InputStream

from . import messages
from . import warnings
from .parser import sa_systemrdl
from .core.ComponentVisitor import RootVisitor
from .core.ExprVisitor import ExprVisitor
from .core.properties import PropertyRuleBook, BuiltinUserProperty
from .core.namespace import NamespaceRegistry
from .core.elaborate import ElabExpressionsListener, PrePlacementValidateListener, LateElabListener
from .core.elaborate import StructuralPlacementListener
from .core.validate import ValidateListener
from .core import expressions as expr
from . import component as comp
from . import walker
from .node import RootNode
from . import preprocessor
from . import rdltypes

class RDLCompiler:

    def __init__(self, **kwargs: Any):
        """
        RDLCompiler constructor.

        Parameters
        ----------
        message_printer: :class:`~systemrdl.messages.MessagePrinter`
            Override the default message printer
        warning_flags: int
            Flags to enable warnings. See :ref:`messages_warnings` for more details.
        error_flags: int
            Same as ``warning_flags`` but promote them to errors instead.
        dedent_desc: bool
            Automatically remove any common indentation from multi-line
            ``desc`` properties.

            Set to True by default.
        extended_dpa_type_names: bool
            Enable extended type name generation that accounts for dynamic
            property assignments augmenting the type.

            Set to True by default.

            See :ref:`dpa_type_generation` for more details.
        perl_safe_opcodes: list
            Perl preprocessor commands are executed within a
            `Perl Safe <https://perldoc.perl.org/Safe.html>`_ compartment to
            prevent malicious code execution.

            The default set of `Perl opcodes <https://perldoc.perl.org/Opcode.html#Predefined-Opcode-Tags>`_
            allowed should be sufficient for most applications, however this
            option is exposed in the rare case it is necessary to override the
            opcode list in order to make an exception.

            Default value::

                [
                    ':base_core', ':base_mem', ':base_loop', ':base_orig', ':base_math',
                    ':base_thread', ':filesys_read', ':sys_db', ':load',
                    'sort', 'tied', 'pack', 'unpack', 'reset'
                ]


        .. versionchanged:: 1.8
            Added ``dedent_desc`` option.
        .. versionchanged:: 1.9
            Added ``extended_dpa_type_names`` option.
        .. versionchanged:: 1.10
            Added ``perl_safe_opcodes`` option.
        """
        self.env = RDLEnvironment(kwargs)

        # Check for stray kwargs
        if kwargs:
            raise TypeError("got an unexpected keyword argument '%s'" % list(kwargs.keys())[0])

        self.msg = self.env.msg
        self.namespace = NamespaceRegistry(self.env) # type: NamespaceRegistry
        self.visitor = RootVisitor(self)
        self.root = self.visitor.component # type: comp.Root # type: ignore

    def define_udp(self, name, valid_type, valid_components=None, default=None):
        # type: (str, List[Any], Optional[Set[Type[comp.Component]]], Any) -> None
        """
        Pre-define a user-defined property.

        This is the equivalent to the following RDL:

        .. code-block:: none

            property <name> {
                type = <valid_type>;
                component = <valid_components>;
                default = <default>
            };

        Parameters
        ----------
        name: str
            Property name
        valid_components: set
            Set of :class:`~systemrdl.component.Component` types the UDP can be bound to.
            If None, then UDP can be bound to all components.
        valid_type: type
            Assignment type that this UDP will enforce
        default:
            Default if a value is not specified when the UDP is bound to a component.
            Value must be compatible with ``valid_type``

        """
        if valid_components is None:
            valid_components = {
                comp.Field,
                comp.Reg,
                comp.Regfile,
                comp.Addrmap,
                comp.Mem,
                comp.Signal,
                #TODO constraint,
            }

        if name in self.env.property_rules.rdl_properties:
            raise ValueError("name '%s' conflicts with existing built-in RDL property")

        udp = BuiltinUserProperty(self.env, name, valid_components, (valid_type,), default)

        self.env.property_rules.user_properties[udp.name] = udp


    def list_udps(self) -> List[str]:
        """
        List all user-defined properties encountered by the compiler.


        .. versionadded:: 1.12
        """
        return list(self.env.property_rules.user_properties.keys())


    def compile_file(self, path: str, incl_search_paths: Optional[List[str]]=None) -> None:
        """
        Parse & compile a single file and append it to RDLCompiler's root
        namespace.

        If any exceptions (:class:`~systemrdl.RDLCompileError` or other)
        occur during compilation, then the RDLCompiler object should be discarded.

        Parameters
        ----------
        path:str
            Path to an RDL source file

        incl_search_paths:list
            List of additional paths to search to resolve includes.
            If unset, defaults to an empty list.

            Relative include paths are resolved in the following order:

            1. Search each path specified in ``incl_search_paths``.
            2. Path relative to the source file performing the include.

        Raises
        ------
        RDLCompileError
            If any fatal compile error is encountered.
        """

        if incl_search_paths is None:
            incl_search_paths = []

        input_stream = preprocessor.preprocess_file(self.env, path, incl_search_paths)

        # Run Antlr parser on input
        parsed_tree = sa_systemrdl.parse(
            input_stream,
            "root",
            messages.RdlSaErrorListener(self.msg)
        )

        if self.msg.had_error:
            self.msg.fatal("Parse aborted due to previous errors")

        # Traverse parse tree with RootVisitor
        self.visitor.visit(parsed_tree)

        # Reset default property assignments from namespace.
        # They should not be shared between files since that would be confusing.
        self.namespace.default_property_ns_stack = [{}]

        if self.msg.had_error:
            self.msg.fatal("Compile aborted due to previous errors")

    def elaborate(self, top_def_name: Optional[str]=None, inst_name: Optional[str]=None, parameters: Optional[Dict[str, rdltypes.RDLValue]]=None) -> RootNode:
        """
        Elaborates the design for the given top-level addrmap component.

        During elaboration, the following occurs:

        - An instance of the ``$root`` meta-component is created.
        - The addrmap component specified by ``top_def_name`` is instantiated as a
          child of ``$root``.
        - Expressions, parameters, and inferred address/field placements are elaborated.
        - Validation checks are performed.

        If a design contains multiple root-level addrmaps, ``elaborate()`` can be
        called multiple times in order to elaborate each individually.

        If any exceptions (:class:`~systemrdl.RDLCompileError` or other)
        occur during elaboration, then the RDLCompiler object should be discarded.

        Parameters
        ----------
        top_def_name: str
            Explicitly choose which addrmap  in the root namespace will be the
            top-level component.

            If unset, The last addrmap defined will be chosen.

        inst_name: str
            Overrides the top-component's instantiated name.
            By default, instantiated name is the same as ``top_def_name``

        parameters: dict
            Dictionary of parameter overrides for the top component instance.

        Raises
        ------
        RDLCompileError
            If any fatal elaboration error is encountered

        Returns
        -------
        :class:`~systemrdl.node.RootNode`
            Elaborated root meta-component's Node object.
        """
        if parameters is None:
            parameters = {}

        # Get top-level component definition to elaborate
        if top_def_name is not None:
            # Lookup top_def_name
            if top_def_name not in self.root.comp_defs:
                self.msg.fatal("Elaboration target '%s' not found" % top_def_name)
            top_def = self.root.comp_defs[top_def_name]

            if not isinstance(top_def, comp.Addrmap):
                self.msg.fatal("Elaboration target '%s' is not an 'addrmap' component" % top_def_name)
        else:
            # Not specified. Find the last addrmap defined
            for comp_def in reversed(self.root.comp_defs.values()):
                if isinstance(comp_def, comp.Addrmap):
                    top_def = comp_def
                    top_def_name = comp_def.type_name
                    break
            else:
                self.msg.fatal("Could not find any 'addrmap' components to elaborate")

        # Create an instance of the root component
        root_inst = self.root._copy_for_inst({})
        root_inst.is_instance = True
        root_inst.original_def = self.root
        root_inst.inst_name = "$root"

        # Create a top-level instance
        top_inst = top_def._copy_for_inst({})
        top_inst.is_instance = True
        top_inst.original_def = top_def
        top_inst.addr_offset = 0
        top_inst.external = True # addrmap is always implied as external
        if inst_name is not None:
            top_inst.inst_name = inst_name
        else:
            top_inst.inst_name = top_def_name

        # Override parameters as needed
        for param_name, value in parameters.items():
            # Find the parameter to override
            parameter = None
            for p in top_inst.parameters:
                if p.name == param_name:
                    parameter = p
                    break
            else:
                raise ValueError("Parameter '%s' is not available for override" % param_name)

            literal_expr = expr.ExternalLiteral(self.env, value)
            assign_expr = expr.AssignmentCast(self.env, None, literal_expr, parameter.param_type)
            assign_type = assign_expr.predict_type()
            if assign_type is None:
                raise TypeError("Incorrect type for parameter '%s'" % param_name)

            parameter.expr = assign_expr


        # instantiate top_inst into the root component instance
        root_inst.children.append(top_inst)

        root_node = RootNode(root_inst, self.env, None)

        # Resolve all expressions
        walker.RDLWalker(skip_not_present=False).walk(
            root_node,
            ElabExpressionsListener(self.msg)
        )

        # Resolve address and field placement
        walker.RDLWalker(skip_not_present=False).walk(
            root_node,
            PrePlacementValidateListener(self.msg),
            StructuralPlacementListener(self.msg),
            LateElabListener(self.msg, self.env)
        )

        # Validate design
        # Only need to validate nodes that are present
        walker.RDLWalker(skip_not_present=True).walk(root_node, ValidateListener(self.env))

        if self.msg.had_error:
            self.msg.fatal("Elaborate aborted due to previous errors")

        return root_node


    def eval(self, expression: str) -> rdltypes.RDLValue:
        """
        Evaluate an RDL expression string and return its compiled value.
        This function is provided as a helper to simplify overriding top-level
        parameters during elaboration.

        Parameters
        ----------
        expression: str
            This string is parsed and evaluated as a SystemRDL expression.
            Any references used in the expression are resolved using the
            current contents of the root namespace.

        Raises
        ------
        ValueError
            If any parse or evaluation error occurs.


        .. versionadded:: 1.8
        """
        # Create local message handler that suppresses the usual ouput
        # to stderr.
        # Instead raises ValueError on any error
        msg_printer = messages.MessageExceptionRaiser()
        msg_handler = messages.MessageHandler(msg_printer)

        input_stream = InputStream(expression)

        parsed_tree = sa_systemrdl.parse(
            input_stream,
            "expr",
            messages.RdlSaErrorListener(self.msg)
        )

        visitor = ExprVisitor(self)

        # override visitor to use local message handler
        visitor.msg = msg_handler

        result = visitor.visit(parsed_tree)
        result.predict_type()
        return result.get_value()


class RDLEnvironment:
    """
    Container object for misc resources that are preserved outside the lifetime
    of source compilation
    """
    def __init__(self, args_dict: Dict[str, Any]):

        # Collect args
        message_printer = args_dict.pop('message_printer', messages.MessagePrinter())
        w_flags = args_dict.pop('warning_flags', 0)
        e_flags = args_dict.pop('error_flags', 0)
        self.dedent_desc = args_dict.pop('dedent_desc', True)
        self.use_extended_type_name_gen = args_dict.pop('extended_dpa_type_names', True)
        self.perl_safe_opcodes = args_dict.pop('perl_safe_opcodes', [
            ':base_core', ':base_mem', ':base_loop', ':base_orig', ':base_math',
            ':base_thread', ':filesys_read', ':sys_db', ':load',
            'sort', 'tied', 'pack', 'unpack', 'reset'
        ])

        self.chk_missing_reset = self.chk_flag_severity(warnings.MISSING_RESET, w_flags, e_flags)
        self.chk_implicit_field_pos = self.chk_flag_severity(warnings.IMPLICIT_FIELD_POS, w_flags, e_flags)
        self.chk_implicit_addr = self.chk_flag_severity(warnings.IMPLICIT_ADDR, w_flags, e_flags)
        self.chk_stride_not_pow2 = self.chk_flag_severity(warnings.STRIDE_NOT_POW2, w_flags, e_flags)
        self.chk_strict_self_align = self.chk_flag_severity(warnings.STRICT_SELF_ALIGN, w_flags, e_flags)
        self.chk_sparse_reg_stride = self.chk_flag_severity(warnings.SPARSE_REG_STRIDE, w_flags, e_flags)

        self.msg = messages.MessageHandler(message_printer)
        self.property_rules = PropertyRuleBook(self)

    @staticmethod
    def chk_flag_severity(flag: int, w_flags: int, e_flags: int) -> messages.Severity:
        if bool(e_flags & flag):
            return messages.Severity.ERROR
        elif bool(w_flags & flag):
            return messages.Severity.WARNING
        else:
            return messages.Severity.NONE
