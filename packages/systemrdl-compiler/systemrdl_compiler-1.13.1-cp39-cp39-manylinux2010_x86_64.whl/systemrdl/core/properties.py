from typing import Any, Set, Type, Iterable, TYPE_CHECKING, Optional, Dict, List

from .. import component as comp
from .. import node as m_node
from .. import rdltypes
from . import expressions

if TYPE_CHECKING:
    from ..compiler import RDLEnvironment
    from ..source_ref import SourceRefBase

def get_all_subclasses(cls: type) -> List[type]:
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__()
        for g in get_all_subclasses(s)
    ]

#===============================================================================
# Base property
#===============================================================================
class PropertyRule:
    # Set of components this property can be bound to
    bindable_to = set() # type: Set[Type[comp.Component]]

    # List of valid assignment types. In order of cast preference
    valid_types = tuple() # type: Iterable[Any]

    # Default value if not assigned
    default = None # type: Any

    # Whether dynamic assignments are allowed to be made to this property
    dyn_assign_allowed= True # type: bool

    # Group string in which this property is mutually exclusive
    mutex_group = None # type: Optional[str]

    #---------------------------------------------------------------------------
    def __init__(self, env: 'RDLEnvironment'):
        self.env = env

    #---------------------------------------------------------------------------
    def get_name(self) -> str:
        return type(self).__name__.replace("Prop_", "")

    #---------------------------------------------------------------------------
    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Used by the compiler for either local or dynamic prop assignments
        This does the following:
            - Check that the property is allowed in this component
            - Check if the value being assigned is compatible
            - Assign the property, as well as any side-effects
                subclasses extend this to define prop-specific side-effects
        """

        # Check if property is allowed in this component
        if type(comp_def) not in self.bindable_to:
            self.env.msg.fatal(
                "The property '%s' is not valid for '%s' components"
                % (self.get_name(), type(comp_def).__name__.lower()),
                src_ref
            )

        # Property assignments with no rhs show up as None here
        # For built-in properties, this implies a True value
        if value is None:
            value = True

        # unpack true type of value
        # Contents of value can be:
        #   - An expression (instance of an Expr subclass)
        #   - Direct assignment of a type-compatible value
        if isinstance(value, expressions.Expr):
            # Predict expected type after value would get evaluated
            assign_type = value.predict_type()
        elif rdltypes.is_user_enum(value):
            # Value is a user enum type derived from UserEnum.
            # Mark it as such
            assign_type = rdltypes.UserEnum
        else:
            # Value is already evaluated
            assign_type = type(value)

        # Check if value's type is compatible
        for valid_type in self.valid_types:
            if expressions.is_castable(assign_type, valid_type):
                if isinstance(value, expressions.Expr):
                    # Found a type-compatible match. (first match is best match)
                    # Wrap the expression with an explicit assignment cast
                    value = expressions.AssignmentCast(self.env, src_ref, value, valid_type)
                break
        else:
            self.env.msg.fatal(
                "Incompatible assignment to property '%s'" % self.get_name(),
                src_ref
            )

        # Store the property
        comp_def.properties[self.get_name()] = value

        if src_ref is not None:
            comp_def.property_src_ref[self.get_name()] = src_ref

    #---------------------------------------------------------------------------
    def get_default(self, node: m_node.Node) -> Any:
        # pylint: disable=unused-argument
        """
        Used when the user queries a property, and it was not explicitly set.
        Default values are not always directly known. Sometimes they depend on
        one or more other properties.
        The base behavior will simply return the static variable's value.
        Properties with more complex rules can override this to implement
        other default value derivations
        """
        return self.default

    #---------------------------------------------------------------------------
    def validate(self, node: m_node.Node, value: Any) -> None:
        """
        Used during the validate phase after elaboration.
        Performs checks against the property's value
        """

    #---------------------------------------------------------------------------
    def _validate_ref_width(self, node: m_node.VectorNode, value: Any) -> None:
        """
        Helper function to check that if value is a vector-like reference,
        that it's width matches the node.
        """
        if isinstance(value, m_node.VectorNode):
            if node.width != value.width:
                self.env.msg.error(
                    "%s '%s' references %s '%s''s value but they are not the same width (%d != %d)"
                    % (
                        type(node.inst).__name__.lower(), node.inst_name,
                        type(value.inst).__name__.lower(), value.inst_name,
                        node.width, value.width
                    ),
                    node.inst.inst_src_ref
                )

    #---------------------------------------------------------------------------
    def _validate_ref_width_is_1(self, node: m_node.Node, value: Any) -> None:
        """
        Helper function to check that if value is a vector-like reference,
        that it's width is exactly 1.
        """
        if isinstance(value, m_node.VectorNode):
            if value.width != 1:
                self.env.msg.error(
                    "%s '%s' references %s '%s' but it's width is not 1"
                    % (
                        type(node.inst).__name__.lower(), node.inst_name,
                        type(value.inst).__name__.lower(), value.inst_name
                    ),
                    node.inst.inst_src_ref
                )

#===============================================================================
class PropertyRuleBoolPair(PropertyRule):
    # Property name of the equivalent opposite
    opposite_property = ""


    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Side effect: Ensure assignment of the opposite is cleared since it is being
        overridden
        """
        super().assign_value(comp_def, value, src_ref)
        if self.opposite_property in comp_def.properties:
            del comp_def.properties[self.opposite_property]

    def get_default(self, node: m_node.Node) -> bool:
        """
        If not explicitly set, check if the opposite was set first before returning
        default
        """
        if self.opposite_property in node.inst.properties:
            return not node.inst.properties[self.opposite_property]
        else:
            return self.default

#===============================================================================
# General Properties
#===============================================================================
class Prop_name(PropertyRule):
    """
    Specifies a more descriptive name
    (5.2.1)
    """
    bindable_to = {comp.Addrmap, comp.Field, comp.Mem, comp.Reg, comp.Regfile, comp.Signal}
    valid_types = (str,)
    default = ""
    dyn_assign_allowed = True
    mutex_group = None

    def get_default(self, node: m_node.Node) -> str:
        """
        If name is undefined, it is presumed to be the instance name.
        (5.2.1.1)
        """
        return node.inst_name


class Prop_desc(PropertyRule):
    """
    Describes the component’s purpose.
    (5.2.1)
    """
    bindable_to = {comp.Addrmap, comp.Field, comp.Mem, comp.Reg, comp.Regfile, comp.Signal}
    valid_types = (str,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

class Prop_dontcompare(PropertyRule):
    """
    Indicates the components read data shall be discarded and not compared
    against expected results.
    (5.2.2)
    """
    bindable_to = {comp.Addrmap, comp.Reg, comp.Regfile, comp.Field}
    valid_types = (int, bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "O"

    def validate(self, node: m_node.Node, value: Any) -> None:
        donttest = node.get_property("donttest")

        if isinstance(node, m_node.FieldNode):
            # 5.2.2.1-a: If value is a bit mask, the mask shall have the same width
            # as the field
            if isinstance(value, int):
                if value >= (1 << node.width):
                    self.env.msg.error(
                        "Bit mask (%d) of property 'dontcompare' exceeds width (%d) of field '%s'"
                        % (value, node.width, node.inst_name),
                        node.inst.inst_src_ref
                    )

            # Normalize values to masks
            if isinstance(value, bool):
                if value:
                    value = (1 << node.width) - 1
                else:
                    value = 0
            if isinstance(donttest, bool):
                if donttest:
                    donttest = (1 << node.width) - 1
                else:
                    donttest = 0

            # 5.2.2.1-c.2: dontcompare/donttest cannot have one true and the
            # other non-zero
            # 5.2.2.1-c.3: the bitwise AND of dontcompare/donttest  masks
            # shall be zero (0) for a particular component
            # (i.e., donttest & dontcompare = 0)
            if value & donttest:
                self.env.msg.error(
                    "A field's bit cannot have both 'dontcompare' and 'donttest' properties enabled",
                    node.inst.inst_src_ref
                )

        else:
            # A boolean may end up cast as an int. Normalize 0 or 1 to boolean
            if isinstance(value, int) and value in (0, 1):
                value = bool(value)

            # 5.2.2.1-b: can also be applied to reg, regfile, and addrmap
            # components, but only as a boolean
            if not isinstance(value, bool):
                self.env.msg.error(
                    "Property 'dontcompare' expects a boolean for non-field types. Got an integer in '%s'"
                    % (node.inst_name),
                    node.inst.inst_src_ref
                )

            # 5.2.2.1-c.1: dontcompare/donttest cannot both be set to true
            if donttest and value:
                self.env.msg.error(
                    "Properties dontcompare/donttest cannot both be set to true in '%s'"
                    % (node.inst_name),
                    node.inst.inst_src_ref
                )



class Prop_donttest(PropertyRule):
    """
    Indicates the component is not included in structural testing.
    (5.2.2)
    """
    bindable_to = {comp.Addrmap, comp.Reg, comp.Regfile, comp.Field}
    valid_types = (int, bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "O"

    def validate(self, node: m_node.Node, value: Any) -> None:
        if isinstance(node, m_node.FieldNode):
            # 5.2.2.1-a: If value is a bit mask, the mask shall have the same width
            # as the field
            if isinstance(value, int):
                if value >= (1 << node.width):
                    self.env.msg.error(
                        "Bit mask (%d) of property 'donttest' exceeds width (%d) of field '%s'"
                        % (value, node.width, node.inst_name),
                        node.inst.inst_src_ref
                    )
        else:
            # A boolean may end up cast as an int. Normalize 0 or 1 to boolean
            if isinstance(value, int) and value in (0, 1):
                value = bool(value)

            # 5.2.2.1-b: can also be applied to reg, regfile, and addrmap
            # components, but only as a boolean
            if not isinstance(value, bool):
                self.env.msg.error(
                    "Property 'donttest' expects a boolean for non-field types. Got an integer in '%s'"
                    % (node.inst_name),
                    node.inst.inst_src_ref
                )

class Prop_ispresent(PropertyRule):
    """
    Setting ispresent to false causes the given component instance to be removed
    from the final specification.
    (5.3)
    """
    bindable_to = {comp.Addrmap, comp.Field, comp.Mem, comp.Reg, comp.Regfile, comp.Signal}
    valid_types = (bool,)
    default = True
    dyn_assign_allowed = True
    mutex_group = None

class Prop_errextbus(PropertyRule):
    bindable_to = {comp.Addrmap, comp.Reg, comp.Regfile}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = False
    mutex_group = None

    def validate(self, node: m_node.Node, value: Any) -> None:
        # 10.6.1-h: errextbus is only valid for external registers
        if (node.inst.external is False) and (value is True):
            self.env.msg.error(
                "The 'errextbus' property is set to 'true', but instance '%s' is not external"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

class Prop_hdl_path(PropertyRule):
    bindable_to = {comp.Addrmap, comp.Reg, comp.Regfile}
    valid_types = (str,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

class Prop_hdl_path_gate(PropertyRule):
    bindable_to = {comp.Addrmap, comp.Reg, comp.Regfile}
    valid_types = (str,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

class Prop_hdl_path_gate_slice(PropertyRule):
    bindable_to = {comp.Field, comp.Mem}
    valid_types = (rdltypes.ArrayPlaceholder(str),)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

class Prop_hdl_path_slice(PropertyRule):
    bindable_to = {comp.Field, comp.Mem}
    valid_types = (rdltypes.ArrayPlaceholder(str),)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

#===============================================================================
# Signal Properties
#===============================================================================

class Prop_signalwidth(PropertyRule):
    """
    Width of the signal.
    (8.2)
    """
    bindable_to = {comp.Signal}
    valid_types = (int,)
    default = None
    dyn_assign_allowed = False
    mutex_group = None

    def get_default(self, node: m_node.Node) -> Optional[int]:
        """
        If not explicitly set, inherits the instantiation's width
        """
        assert isinstance(node, m_node.SignalNode)
        return node.width

class Prop_sync(PropertyRuleBoolPair):
    """
    Signal is synchronous to the clock of the component.
    (8.2)
    """
    bindable_to = {comp.Signal}
    valid_types = (bool,)
    default = True
    dyn_assign_allowed = True
    mutex_group = "N"

    opposite_property = "async"

class Prop_async(PropertyRuleBoolPair):
    """
    Signal is asynchronous to the clock of the component.
    (8.2)
    """
    bindable_to = {comp.Signal}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "N"

    opposite_property = "sync"

class Prop_cpuif_reset(PropertyRule):
    """
    Default signal to use for resetting the software interface logic. If
    cpuif_reset is not defined, this reverts to the default reset signal. This
    parameter only controls the CPU interface of a generated slave.
    (8.2)
    """
    bindable_to = {comp.Signal}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_field_reset(PropertyRule):
    """
    Default signal to use for resetting field implementations. If field_reset
    is not defined, this reverts to the default reset signal.
    (8.2)
    """
    bindable_to = {comp.Signal}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_activelow(PropertyRule):
    """
    Signal is active low (state of 0 means ON).
    (8.2)
    """
    bindable_to = {comp.Signal}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "A"

class Prop_activehigh(PropertyRule):
    """
    Signal is active high (state of 1 means ON).
    (8.2)
    """
    bindable_to = {comp.Signal}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "A"

#===============================================================================
# Field Properties
#===============================================================================

#-------------------------------------------------------------------------------
# Field access Properties
#-------------------------------------------------------------------------------
class Prop_hw(PropertyRule):
    """
    Design’s ability to sample/update a field.
    (9.4)
    """
    bindable_to = {comp.Field}
    valid_types = (rdltypes.AccessType,)
    default = rdltypes.AccessType.rw
    dyn_assign_allowed = False
    mutex_group = None

class Prop_sw(PropertyRule):
    """
    Programmer’s ability to read/write a field.
    (9.4)
    """
    bindable_to = {comp.Field, comp.Mem}
    valid_types = (rdltypes.AccessType,)
    default = rdltypes.AccessType.rw
    dyn_assign_allowed = True
    mutex_group = None

#-------------------------------------------------------------------------------
# Hardware Signal Properties
#-------------------------------------------------------------------------------
class Prop_next(PropertyRule):
    """
    The next value of the field; the D-input for flip-flops.
    (9.5)
    """
    bindable_to = {comp.Field}
    valid_types = (comp.Field, comp.Signal, rdltypes.PropertyReference,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)

        # 9.5.1-e: next cannot be self-referencing
        if isinstance(value, rdltypes.PropertyReference):
            ref_node = value.node
        else:
            ref_node = value

        if node.get_path() == ref_node.get_path():
            self.env.msg.error(
                "Field '%s' cannot reference itself in next property"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

        # Check width
        self._validate_ref_width(node, value)

class Prop_reset(PropertyRule):
    """
    The reset value for the field when resetsignal is asserted.
    (9.5)
    """
    bindable_to = {comp.Field}
    valid_types = (int, comp.Field, comp.Signal,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        if type(value) == int:
            # 9.5.1-c: The reset value cannot be larger than can fit in the field
            if value >= (1 << node.width):
                self.env.msg.error(
                    "The reset value (%d) of field '%s' cannot fit within it's width (%d)"
                    % (value, node.inst_name, node.width),
                    node.inst.inst_src_ref
                )
        elif isinstance(value, m_node.FieldNode):
            # 9.5.1-e: reset cannot be self-referencing
            if node.get_path() == value.get_path():
                self.env.msg.error(
                    "Field '%s' cannot reference itself in reset property"
                    % (node.inst_name),
                    node.inst.inst_src_ref
                )
        elif isinstance(value, m_node.SignalNode):
            pass
        else:
            raise RuntimeError

        # Check width
        # 9.5.1-d: When reset is a reference, it shall reference another
        # field of the same size.
        self._validate_ref_width(node, value)

class Prop_resetsignal(PropertyRule):
    """
    Reference to the signal used to reset the field
    (9.5)
    """
    bindable_to = {comp.Field}
    valid_types = (comp.Signal,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

#-------------------------------------------------------------------------------
# Software access properties
#-------------------------------------------------------------------------------

class Prop_rclr(PropertyRule):
    """
    Clear on read (field = 0).
    (9.6)6
    """
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "P"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Overrides other related properties
        """
        super().assign_value(comp_def, value, src_ref)
        if "rset" in comp_def.properties:
            del comp_def.properties["rset"]
        if "onread" in comp_def.properties:
            del comp_def.properties["onread"]

    def get_default(self, node: m_node.Node) -> bool:
        """
        If not explicitly set, check if onread sets the equivalent
        """
        if node.inst.properties.get("onread", None) == rdltypes.OnReadType.rclr:
            return True
        else:
            return self.default

class Prop_rset(PropertyRule):
    """
    Set on read (field = all 1’s).
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "P"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Overrides other related properties
        """
        super().assign_value(comp_def, value, src_ref)
        if "rclr" in comp_def.properties:
            del comp_def.properties["rclr"]
        if "onread" in comp_def.properties:
            del comp_def.properties["onread"]

    def get_default(self, node: m_node.Node) -> bool:
        """
        If not explicitly set, check if onread sets the equivalent
        """
        if node.inst.properties.get("onread", None) == rdltypes.OnReadType.rset:
            return True
        else:
            return self.default

class Prop_onread(PropertyRule):
    """
    Read side-effect.
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (rdltypes.OnReadType,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "P"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Overrides other related properties
        """
        super().assign_value(comp_def, value, src_ref)
        if "rclr" in comp_def.properties:
            del comp_def.properties["rclr"]
        if "rset" in comp_def.properties:
            del comp_def.properties["rset"]

    def get_default(self, node: m_node.Node) -> Optional[rdltypes.OnReadType]:
        """
        If not explicitly set, check if rset or rclr imply the value
        """
        if node.inst.properties.get("rset", False):
            return rdltypes.OnReadType.rset
        elif node.inst.properties.get("rclr", False):
            return rdltypes.OnReadType.rclr
        else:
            return self.default

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        # 9.6.1-i A field with an onread property shall have software read access
        if (value is not None) and not node.is_sw_readable:
            self.env.msg.error(
                "Field '%s' has an 'onread' property but does not have software read access"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

        # 9.6.1-j A field with an onread value of ruser shall be external
        if (node.inst.external is False) and (value == rdltypes.OnReadType.ruser):
            self.env.msg.error(
                "The 'onread' property is set to 'ruser', but instance '%s' is not external"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Prop_woclr(PropertyRule):
    """
    Write one to clear (field = field & ~write_data).
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "B"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Overrides other related properties
        """
        super().assign_value(comp_def, value, src_ref)
        if "woset" in comp_def.properties:
            del comp_def.properties["woset"]
        if "onwrite" in comp_def.properties:
            del comp_def.properties["onwrite"]

    def get_default(self, node: m_node.Node) -> bool:
        """
        If not explicitly set, check if onwrite sets the equivalent
        """
        if node.inst.properties.get("onwrite", None) == rdltypes.OnWriteType.woclr:
            return True
        else:
            return self.default

class Prop_woset(PropertyRule):
    """
    Write one to set (field = field | write_data).
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "B"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Overrides other related properties
        """
        super().assign_value(comp_def, value, src_ref)
        if "woclr" in comp_def.properties:
            del comp_def.properties["woclr"]
        if "onwrite" in comp_def.properties:
            del comp_def.properties["onwrite"]

    def get_default(self, node: m_node.Node) -> bool:
        """
        If not explicitly set, check if onread sets the equivalent
        """
        if node.inst.properties.get("onwrite", None) == rdltypes.OnWriteType.woset:
            return True
        else:
            return self.default

class Prop_onwrite(PropertyRule):
    """
    Write side-effect
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (rdltypes.OnWriteType,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "B"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Overrides other related properties
        """
        super().assign_value(comp_def, value, src_ref)
        if "woclr" in comp_def.properties:
            del comp_def.properties["woclr"]
        if "woset" in comp_def.properties:
            del comp_def.properties["woset"]

    def get_default(self, node: m_node.Node) -> Optional[rdltypes.OnWriteType]:
        """
        If not explicitly set, check if woset or woclr imply the value
        """
        if node.inst.properties.get("woset", False):
            return rdltypes.OnWriteType.woset
        elif node.inst.properties.get("woclr", False):
            return rdltypes.OnWriteType.woclr
        else:
            return self.default

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        # 9.6.1-l A field with an onwrite property shall have software write access.
        if (value is not None) and not node.is_sw_writable:
            self.env.msg.error(
                "Field '%s' has an 'onwrite' property but does not have software write access"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

        # 9.6.1-m A field with an onwrite value of wuser shall be external
        if (node.inst.external is False) and (value == rdltypes.OnWriteType.wuser):
            self.env.msg.error(
                "The 'onwrite' property is set to 'wuser', but instance '%s' is not external"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Prop_swwe(PropertyRule):
    """
    Override software-writeability of this field.
    Field is writable if signal/field/value is True
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (bool, comp.Signal, comp.Field,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "R"

    def validate(self, node: m_node.Node, value: Any) -> None:
        self._validate_ref_width_is_1(node, value)

class Prop_swwel(PropertyRule):
    """
    Override software-writeability of this field.
    Field is writable if signal/field/value is False
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (bool, comp.Signal, comp.Field,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "R"

    def validate(self, node: m_node.Node, value: Any) -> None:
        self._validate_ref_width_is_1(node, value)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Prop_swmod(PropertyRule):
    """
    Indicates a generated output signal shall notify hardware when this field is
    modified by software
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_swacc(PropertyRule):
    """
    Indicates a generated output signal shall notify hardware when this field is
    accessed by software
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_singlepulse(PropertyRule):
    """
    Field asserts for one cycle when written 1 and then clears back to 0
    on the next cycle
    If set, field shall be instantiated with a width of 1 and the reset value
    shall be specified as 0
    (9.6)
    """
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        # 9.6.1-g: singlepulse fields shall be instantiated with a width of 1
        # and the reset value shall be specified as 0
        if value:
            if node.width != 1:
                self.env.msg.error(
                    "Field '%s' marked as 'singlepulse' shall have width of 1"
                    % (node.inst_name),
                    node.inst.inst_src_ref
                )

            if node.get_property('reset') != 0:
                self.env.msg.error(
                    "Field '%s' marked as 'singlepulse' shall have a reset value of 0"
                    % (node.inst_name),
                    node.inst.inst_src_ref
                )

            # singlepulse does not make sense alongside any onwrite properties
            # that conflict with singlepulse semantics
            onwrite = node.get_property('onwrite')
            if onwrite is not None:
                illegal_onwrite = (
                    rdltypes.OnWriteType.woclr,
                    rdltypes.OnWriteType.wclr,
                )
                if onwrite in illegal_onwrite:
                    self.env.msg.error(
                        "Field '%s' marked as 'singlepulse' has conflicting 'onwrite' value of '%s'"
                        % (node.inst_name, onwrite.name),
                        node.inst.inst_src_ref
                    )

#-------------------------------------------------------------------------------
# Hardware access properties
#-------------------------------------------------------------------------------

class Prop_we(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "C"

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        if value and (node.get_property('hw') not in (rdltypes.AccessType.rw, rdltypes.AccessType.w)):
            self.env.msg.error(
                "Property 'we' is 'true' on field '%s', but the field is not writable by hardware"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

        if value and not node.implements_storage:
            self.env.msg.error(
                "Use of 'we' property on field '%s' that does not implement storage does not make sense"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

class Prop_wel(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "C"

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        if value and (node.get_property('hw') not in (rdltypes.AccessType.rw, rdltypes.AccessType.w)):
            self.env.msg.error(
                "Property 'we' is 'true' on field '%s', but the field is not writable by hardware"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

        if value and not node.implements_storage:
            self.env.msg.error(
                "Use of 'wel' property on field '%s' that does not implement storage does not make sense"
                % (node.inst_name),
                node.inst.inst_src_ref
            )

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Prop_anded(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_ored(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_xored(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Prop_fieldwidth(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int,)
    default = None
    dyn_assign_allowed = False
    mutex_group = None

    def get_default(self, node: m_node.Node) -> Optional[int]:
        """
        If not explicitly set, inherits the instantiation's width
        """
        assert isinstance(node, m_node.FieldNode)
        return node.width

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Prop_hwclr(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_hwset(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Prop_hwenable(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (comp.Field, comp.Signal,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "D"

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        self._validate_ref_width(node, value)

class Prop_hwmask(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (comp.Field, comp.Signal,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "D"

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        self._validate_ref_width(node, value)


#-------------------------------------------------------------------------------
# Counter field properties
#-------------------------------------------------------------------------------

class Prop_counter(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "E"

class Prop_threshold(PropertyRule):
    """
    alias of incrthreshold.
    """
    bindable_to = {comp.Field}
    valid_types = (int, bool, comp.Signal, comp.Field,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "incrthreshold alias"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Set both alias and actual value
        """
        super().assign_value(comp_def, value, src_ref)
        comp_def.properties['incrthreshold'] = comp_def.properties['threshold']

class Prop_saturate(PropertyRule):
    """
    alias of incrsaturate.
    """
    bindable_to = {comp.Field}
    valid_types = (int, bool, comp.Signal, comp.Field,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "incrsaturate alias"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Set both alias and actual value
        """
        super().assign_value(comp_def, value, src_ref)
        comp_def.properties['incrsaturate'] = comp_def.properties['saturate']

class Prop_incrthreshold(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int, bool, comp.Signal, comp.Field,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "incrthreshold alias"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Set both alias and actual value
        """
        super().assign_value(comp_def, value, src_ref)
        comp_def.properties['threshold'] = comp_def.properties['incrthreshold']

class Prop_incrsaturate(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int, bool, comp.Signal, comp.Field,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "incrsaturate alias"

    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        """
        Set both alias and actual value
        """
        super().assign_value(comp_def, value, src_ref)
        comp_def.properties['saturate'] = comp_def.properties['incrsaturate']

class Prop_overflow(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_underflow(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_incr(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (comp.Signal, comp.Field, rdltypes.PropertyReference,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

class Prop_incrvalue(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int, comp.Signal, comp.Field,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "F"

class Prop_incrwidth(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "F"

class Prop_decrvalue(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int, comp.Signal, comp.Field,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "G"

class Prop_decr(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (comp.Signal, comp.Field, rdltypes.PropertyReference,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

class Prop_decrwidth(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "G"

class Prop_decrsaturate(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int, bool, comp.Signal, comp.Field,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

class Prop_decrthreshold(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (int, bool, comp.Signal, comp.Field,)
    default = False
    dyn_assign_allowed = True
    mutex_group = None

#-------------------------------------------------------------------------------
# Field access interrupt properties
#-------------------------------------------------------------------------------

class Prop_intr(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "E"

class Prop_intr_type(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (rdltypes.InterruptType,)
    default = rdltypes.InterruptType.level
    dyn_assign_allowed = True
    mutex_group = None

    def get_name(self) -> str:
        # Interrupt modifier type is a "special" hidden property
        # Intentinally override the property name to something that is impossible
        # to define in RDL and collide with
        # Use of space in an ID works!
        return "intr type"

class Prop_enable(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (comp.Field, comp.Signal,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "J"

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        self._validate_ref_width(node, value)

class Prop_mask(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (comp.Field, comp.Signal,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "J"

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        self._validate_ref_width(node, value)

class Prop_haltenable(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (comp.Field, comp.Signal,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "K"

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        self._validate_ref_width(node, value)

class Prop_haltmask(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (comp.Field, comp.Signal,)
    default = None
    dyn_assign_allowed = True
    mutex_group = "K"

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        self._validate_ref_width(node, value)

class Prop_sticky(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "I"

class Prop_stickybit(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = True
    mutex_group = "I"

    def get_default(self, node: m_node.Node) -> bool:
        """
        Unless specified otherwise, intr fields are implicitly stickybit
        """
        if node.inst.properties.get("intr", False):
            # Interrupt is set!
            # Default is implicitly stickybit, unless the mutually-exclusive
            # sticky property was set instead
            return not node.inst.properties.get("sticky", False)
        else:
            return False


#-------------------------------------------------------------------------------
# Misc properties
#-------------------------------------------------------------------------------
class Prop_encode(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (rdltypes.UserEnum,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

    def validate(self, node: m_node.Node, value: Any) -> None:
        assert isinstance(node, m_node.FieldNode)
        # 9.10.1-b: The enumeration’s values shall fit inside the field width.
        enum_max = max(map(int, value))
        if enum_max >= (1 << node.width):
            self.env.msg.error(
                "Field '%s' is not wide enough to encode as enum '%s'"
                % (node.inst_name, value.__name__),
                node.inst.inst_src_ref
            )

class Prop_precedence(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (rdltypes.PrecedenceType,)
    default = rdltypes.PrecedenceType.sw
    dyn_assign_allowed = True
    mutex_group = None

class Prop_paritycheck(PropertyRule):
    bindable_to = {comp.Field}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = False
    mutex_group = None

#===============================================================================
# Reg Properties
#===============================================================================

class Prop_regwidth(PropertyRule):
    """
    The bit-width of the register (power of two).
    """
    bindable_to = {comp.Reg}
    valid_types = (int,)
    default = 32
    dyn_assign_allowed = False
    mutex_group = None

class Prop_accesswidth(PropertyRule):
    """
    The minimum software access width (power of two) operation that may be
    performed on the register.
    """
    bindable_to = {comp.Reg}
    valid_types = (int,)
    default = None
    dyn_assign_allowed = True
    mutex_group = None

    def get_default(self, node: m_node.Node) -> int:
        """
        10.6.1.d: The default value of the accesswidth property shall be
        identical to the width of the register.
        """
        return node.get_property('regwidth')

class Prop_shared(PropertyRule):
    bindable_to = {comp.Reg}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = False
    mutex_group = None

#===============================================================================
# Mem Properties
#===============================================================================

class Prop_mementries(PropertyRule):
    bindable_to = {comp.Mem}
    valid_types = (int,)
    default = 1
    dyn_assign_allowed = False
    mutex_group = None

class Prop_memwidth(PropertyRule):
    bindable_to = {comp.Mem}
    valid_types = (int,)
    default = 32
    dyn_assign_allowed = False
    mutex_group = None

#===============================================================================
# Register file properties
#===============================================================================

class Prop_alignment(PropertyRule):
    bindable_to = {comp.Addrmap, comp.Regfile}
    valid_types = (int,)
    default = None
    dyn_assign_allowed = False
    mutex_group = None

    # RDL spec claims that if unspecified, the default alignment is based on
    # the registers width.
    # If that is taken at face-value, then it would directly conflict with the
    # 'compact' addressing rules in the situation where accesswidth < regwidth
    # Since the equivalent alignment is already handled by the addressing mode
    # rules, the alignment property's default is intentionally left as None
    # in order to distinguish it as unspecified by the user.

class Prop_sharedextbus(PropertyRule):
    bindable_to = {comp.Addrmap, comp.Regfile}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = False
    mutex_group = None
#===============================================================================
# Address map properties
#===============================================================================

class Prop_bigendian(PropertyRuleBoolPair):
    bindable_to = {comp.Addrmap}
    valid_types = (bool,)
    default = False # Default both to false unless one is explicitly set
    dyn_assign_allowed = True
    mutex_group = "L"

    opposite_property = "littleendian"

class Prop_littleendian(PropertyRuleBoolPair):
    bindable_to = {comp.Addrmap}
    valid_types = (bool,)
    default = False # Default both to false unless one is explicitly set
    dyn_assign_allowed = True
    mutex_group = "L"

    opposite_property = "bigendian"

class Prop_addressing(PropertyRule):
    bindable_to = {comp.Addrmap}
    valid_types = (rdltypes.AddressingType,)
    default = rdltypes.AddressingType.regalign
    dyn_assign_allowed = False
    mutex_group = None

class Prop_rsvdset(PropertyRule):
    """
    If true, the read value of all fields not explicitly defined is set to 1
    otherwise, it is set to 0.
    """
    bindable_to = {comp.Addrmap}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = False
    mutex_group = "Q"

class Prop_rsvdsetX(PropertyRule):
    bindable_to = {comp.Addrmap}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = False
    mutex_group = "Q"

class Prop_msb0(PropertyRuleBoolPair):
    bindable_to = {comp.Addrmap}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = False
    mutex_group = "M"

    opposite_property = "lsb0"

class Prop_lsb0(PropertyRuleBoolPair):
    bindable_to = {comp.Addrmap}
    valid_types = (bool,)
    default = True
    dyn_assign_allowed = False
    mutex_group = "M"

    opposite_property = "msb0"

#-------------------------------------------------------------------------------
class Prop_bridge(PropertyRule):
    bindable_to = {comp.Addrmap}
    valid_types = (bool,)
    default = False
    dyn_assign_allowed = False
    mutex_group = None

#===============================================================================
# User-defined property
#===============================================================================

class UserProperty(PropertyRule):
    def __init__(self, env, name, bindable_to, valid_types, default=None, constr_componentwidth=False):
        # type: (RDLEnvironment, str, Set[Type[comp.Component]], Iterable[Any], Any, bool) -> None
        super().__init__(env)

        self.name = name
        self.bindable_to = bindable_to
        self.valid_types = valid_types
        self.default = default
        self.constr_componentwidth = constr_componentwidth

    def get_name(self) -> str:
        return self.name


    def assign_value(self, comp_def: comp.Component, value: Any, src_ref: 'SourceRefBase') -> None:
        # Property assignments with no rhs show up as None here
        # For user-defined properties, this implies the default value
        # (15.2.2)
        if value is None:

            if self.default is None:
                # No default was set. Skip assignment entirely
                return

            value = self.default

        super().assign_value(comp_def, value, src_ref)

    def get_default(self, node: m_node.Node) -> Any:
        # pylint: disable=unused-argument

        # If a user-defined property is not explicitly assigned, then it
        # does not get bound with its default value
        return None

    def validate(self, node: m_node.Node, value: Any) -> None:
        if self.constr_componentwidth:
            # 15.1.1-g: If constraint is set to componentwidth, the assigned
            #   value of the property shall not have a value of 1 for any bit
            #   beyond the width of the field.

            # Spec does not specify, but assuming this check gets ignored for
            # non-vector nodes
            if isinstance(node, m_node.VectorNode):
                if value >= (1 << node.width):
                    self.env.msg.error(
                        "Value (%d) of the '%s' property cannot fit within the width (%d) of component '%s'"
                        % (value, self.name, node.width, node.inst_name),
                        node.inst.inst_src_ref
                    )


class BuiltinUserProperty(UserProperty):
    """
    Specialization of UserProperty for UDPs that are pre-defined by the
    application.
    """

#===============================================================================
# Property References
#===============================================================================

#-------------------------------------------------------------------------------
# Reductions
#-------------------------------------------------------------------------------
class PropRef_anded(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_ored(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_xored(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

#-------------------------------------------------------------------------------
# Counter
#-------------------------------------------------------------------------------
class CounterPropRef(rdltypes.PropertyReference):
    def _validate(self) -> None:
        if not self.node.get_property("counter"):
            self.env.msg.error(
                "Property reference '%s' is illegal because '%s' is not a counter"
                % (self.name, self.node.inst_name),
                self.src_ref
            )

class PropRef_incr(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_incrsaturate(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_incrthreshold(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_incrvalue(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_decr(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_decsaturate(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_decthreshold(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_decrvalue(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_overflow(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_underflow(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_threshold(CounterPropRef):
    allowed_inst_type = comp.Field

class PropRef_saturate(CounterPropRef):
    allowed_inst_type = comp.Field

#-------------------------------------------------------------------------------
# Access
#-------------------------------------------------------------------------------
class PropRef_swacc(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_swmod(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_swwe(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_swwel(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

#-------------------------------------------------------------------------------
# HW Signals
#-------------------------------------------------------------------------------
class PropRef_we(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_wel(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_hwset(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_hwclr(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

#-------------------------------------------------------------------------------
# Interrupts
#-------------------------------------------------------------------------------
class PropRef_intr(rdltypes.PropertyReference):
    allowed_inst_type = comp.Reg

class PropRef_enable(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_halt(rdltypes.PropertyReference):
    allowed_inst_type = comp.Reg

class PropRef_haltenable(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_haltmask(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_mask(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

#-------------------------------------------------------------------------------
class PropRef_hwenable(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_hwmask(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_next(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_reset(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

class PropRef_resetsignal(rdltypes.PropertyReference):
    allowed_inst_type = comp.Field

#===============================================================================
# Property Rulebook
#===============================================================================

class PropertyRuleBook:
    def __init__(self, env: 'RDLEnvironment'):
        self.env = env

        # Auto-discover all properties defined below and load into dict
        self.rdl_properties = {} # type: Dict[str, PropertyRule]
        for prop in get_all_subclasses(PropertyRule):
            if prop.__name__.startswith("Prop_"):
                prop_inst = prop(self.env)
                self.rdl_properties[prop_inst.get_name()] = prop(self.env)

        self.user_properties = {} # type: Dict[str, UserProperty]

        self.rdl_prop_refs = {} # type: Dict[str, Type[rdltypes.PropertyReference]]
        for prop_ref in get_all_subclasses(rdltypes.PropertyReference):
            if prop_ref.__name__.startswith("PropRef_"):
                prop_name = prop_ref.get_name() # type: ignore
                self.rdl_prop_refs[prop_name] = prop_ref

    def lookup_property(self, prop_name: str) -> Optional[PropertyRule]:
        if prop_name in self.rdl_properties:
            return self.rdl_properties[prop_name]
        elif prop_name in self.user_properties:
            return self.user_properties[prop_name]
        else:
            return None

    def lookup_prop_ref_type(self, prop_ref_name):
        # type: (str) -> Optional[Type[rdltypes.PropertyReference]]
        return self.rdl_prop_refs.get(prop_ref_name, None)

    def register_udp(self, udp: UserProperty, src_ref: 'SourceRefBase') -> None:
        if udp.name in self.user_properties:
            self.env.msg.fatal(
                "Multiple declarations of user-defined property '%s'"
                % udp.name,
                src_ref
            )

        if udp.name in self.rdl_properties:
            self.env.msg.fatal(
                "User-defined property '%s' cannot be the same name as a built-in SystemRDL property"
                % udp.name,
                src_ref
            )

        self.user_properties[udp.name] = udp
