/*
 * This file was auto-generated by speedy-antlr-tool v1.0.0
 *  https://github.com/amykyta3/speedy-antlr-tool
 */

#pragma once

#include "SystemRDLBaseVisitor.h"
#include "speedy_antlr.h"

class SA_SystemRDLTranslator : public SystemRDLBaseVisitor {
    speedy_antlr::Translator *translator;

    // Cached context classes
    PyObject *RootContext_cls = NULL;
    PyObject *Root_elemContext_cls = NULL;
    PyObject *Component_defContext_cls = NULL;
    PyObject *Explicit_component_instContext_cls = NULL;
    PyObject *Component_inst_aliasContext_cls = NULL;
    PyObject *Component_named_defContext_cls = NULL;
    PyObject *Component_anon_defContext_cls = NULL;
    PyObject *Component_bodyContext_cls = NULL;
    PyObject *Component_body_elemContext_cls = NULL;
    PyObject *Component_instsContext_cls = NULL;
    PyObject *Component_instContext_cls = NULL;
    PyObject *Field_inst_resetContext_cls = NULL;
    PyObject *Inst_addr_fixedContext_cls = NULL;
    PyObject *Inst_addr_strideContext_cls = NULL;
    PyObject *Inst_addr_alignContext_cls = NULL;
    PyObject *Component_inst_typeContext_cls = NULL;
    PyObject *Component_typeContext_cls = NULL;
    PyObject *Component_type_primaryContext_cls = NULL;
    PyObject *Param_defContext_cls = NULL;
    PyObject *Param_def_elemContext_cls = NULL;
    PyObject *Param_instContext_cls = NULL;
    PyObject *Param_assignmentContext_cls = NULL;
    PyObject *BinaryExprContext_cls = NULL;
    PyObject *UnaryExprContext_cls = NULL;
    PyObject *NOPContext_cls = NULL;
    PyObject *TernaryExprContext_cls = NULL;
    PyObject *Expr_primaryContext_cls = NULL;
    PyObject *ConcatenateContext_cls = NULL;
    PyObject *ReplicateContext_cls = NULL;
    PyObject *Paren_exprContext_cls = NULL;
    PyObject *CastWidthContext_cls = NULL;
    PyObject *CastTypeContext_cls = NULL;
    PyObject *Cast_width_exprContext_cls = NULL;
    PyObject *Range_suffixContext_cls = NULL;
    PyObject *Array_suffixContext_cls = NULL;
    PyObject *Array_type_suffixContext_cls = NULL;
    PyObject *Data_typeContext_cls = NULL;
    PyObject *Basic_data_typeContext_cls = NULL;
    PyObject *LiteralContext_cls = NULL;
    PyObject *NumberHexContext_cls = NULL;
    PyObject *NumberVerilogContext_cls = NULL;
    PyObject *NumberIntContext_cls = NULL;
    PyObject *String_literalContext_cls = NULL;
    PyObject *Boolean_literalContext_cls = NULL;
    PyObject *Array_literalContext_cls = NULL;
    PyObject *Struct_literalContext_cls = NULL;
    PyObject *Struct_kvContext_cls = NULL;
    PyObject *Enum_literalContext_cls = NULL;
    PyObject *Accesstype_literalContext_cls = NULL;
    PyObject *Onreadtype_literalContext_cls = NULL;
    PyObject *Onwritetype_literalContext_cls = NULL;
    PyObject *Addressingtype_literalContext_cls = NULL;
    PyObject *Precedencetype_literalContext_cls = NULL;
    PyObject *Instance_refContext_cls = NULL;
    PyObject *Instance_ref_elementContext_cls = NULL;
    PyObject *Prop_refContext_cls = NULL;
    PyObject *Local_property_assignmentContext_cls = NULL;
    PyObject *Dynamic_property_assignmentContext_cls = NULL;
    PyObject *Normal_prop_assignContext_cls = NULL;
    PyObject *Encode_prop_assignContext_cls = NULL;
    PyObject *Prop_mod_assignContext_cls = NULL;
    PyObject *Prop_assignment_rhsContext_cls = NULL;
    PyObject *Prop_keywordContext_cls = NULL;
    PyObject *Prop_modContext_cls = NULL;
    PyObject *Udp_defContext_cls = NULL;
    PyObject *Udp_attrContext_cls = NULL;
    PyObject *Udp_typeContext_cls = NULL;
    PyObject *Udp_data_typeContext_cls = NULL;
    PyObject *Udp_usageContext_cls = NULL;
    PyObject *Udp_comp_typeContext_cls = NULL;
    PyObject *Udp_defaultContext_cls = NULL;
    PyObject *Udp_constraintContext_cls = NULL;
    PyObject *Enum_defContext_cls = NULL;
    PyObject *Enum_entryContext_cls = NULL;
    PyObject *Enum_prop_assignContext_cls = NULL;
    PyObject *Struct_defContext_cls = NULL;
    PyObject *Struct_elemContext_cls = NULL;
    PyObject *Struct_typeContext_cls = NULL;
    PyObject *Constraint_defContext_cls = NULL;
    PyObject *Constraint_named_defContext_cls = NULL;
    PyObject *Constraint_anon_defContext_cls = NULL;
    PyObject *Constraint_bodyContext_cls = NULL;
    PyObject *Constraint_body_elemContext_cls = NULL;
    PyObject *Constraint_instsContext_cls = NULL;
    PyObject *Constr_relationalContext_cls = NULL;
    PyObject *Constr_prop_assignContext_cls = NULL;
    PyObject *Constr_inside_valuesContext_cls = NULL;
    PyObject *Constr_inside_enumContext_cls = NULL;
    PyObject *Constr_lhsContext_cls = NULL;
    PyObject *Constr_inside_valueContext_cls = NULL;

    public:
    SA_SystemRDLTranslator(speedy_antlr::Translator *translator);
    ~SA_SystemRDLTranslator();
    antlrcpp::Any visitRoot(SystemRDLParser::RootContext *ctx);

    antlrcpp::Any visitRoot_elem(SystemRDLParser::Root_elemContext *ctx);

    antlrcpp::Any visitComponent_def(SystemRDLParser::Component_defContext *ctx);

    antlrcpp::Any visitExplicit_component_inst(SystemRDLParser::Explicit_component_instContext *ctx);

    antlrcpp::Any visitComponent_inst_alias(SystemRDLParser::Component_inst_aliasContext *ctx);

    antlrcpp::Any visitComponent_named_def(SystemRDLParser::Component_named_defContext *ctx);

    antlrcpp::Any visitComponent_anon_def(SystemRDLParser::Component_anon_defContext *ctx);

    antlrcpp::Any visitComponent_body(SystemRDLParser::Component_bodyContext *ctx);

    antlrcpp::Any visitComponent_body_elem(SystemRDLParser::Component_body_elemContext *ctx);

    antlrcpp::Any visitComponent_insts(SystemRDLParser::Component_instsContext *ctx);

    antlrcpp::Any visitComponent_inst(SystemRDLParser::Component_instContext *ctx);

    antlrcpp::Any visitField_inst_reset(SystemRDLParser::Field_inst_resetContext *ctx);

    antlrcpp::Any visitInst_addr_fixed(SystemRDLParser::Inst_addr_fixedContext *ctx);

    antlrcpp::Any visitInst_addr_stride(SystemRDLParser::Inst_addr_strideContext *ctx);

    antlrcpp::Any visitInst_addr_align(SystemRDLParser::Inst_addr_alignContext *ctx);

    antlrcpp::Any visitComponent_inst_type(SystemRDLParser::Component_inst_typeContext *ctx);

    antlrcpp::Any visitComponent_type(SystemRDLParser::Component_typeContext *ctx);

    antlrcpp::Any visitComponent_type_primary(SystemRDLParser::Component_type_primaryContext *ctx);

    antlrcpp::Any visitParam_def(SystemRDLParser::Param_defContext *ctx);

    antlrcpp::Any visitParam_def_elem(SystemRDLParser::Param_def_elemContext *ctx);

    antlrcpp::Any visitParam_inst(SystemRDLParser::Param_instContext *ctx);

    antlrcpp::Any visitParam_assignment(SystemRDLParser::Param_assignmentContext *ctx);

    antlrcpp::Any visitBinaryExpr(SystemRDLParser::BinaryExprContext *ctx);

    antlrcpp::Any visitUnaryExpr(SystemRDLParser::UnaryExprContext *ctx);

    antlrcpp::Any visitNOP(SystemRDLParser::NOPContext *ctx);

    antlrcpp::Any visitTernaryExpr(SystemRDLParser::TernaryExprContext *ctx);

    antlrcpp::Any visitExpr_primary(SystemRDLParser::Expr_primaryContext *ctx);

    antlrcpp::Any visitConcatenate(SystemRDLParser::ConcatenateContext *ctx);

    antlrcpp::Any visitReplicate(SystemRDLParser::ReplicateContext *ctx);

    antlrcpp::Any visitParen_expr(SystemRDLParser::Paren_exprContext *ctx);

    antlrcpp::Any visitCastWidth(SystemRDLParser::CastWidthContext *ctx);

    antlrcpp::Any visitCastType(SystemRDLParser::CastTypeContext *ctx);

    antlrcpp::Any visitCast_width_expr(SystemRDLParser::Cast_width_exprContext *ctx);

    antlrcpp::Any visitRange_suffix(SystemRDLParser::Range_suffixContext *ctx);

    antlrcpp::Any visitArray_suffix(SystemRDLParser::Array_suffixContext *ctx);

    antlrcpp::Any visitArray_type_suffix(SystemRDLParser::Array_type_suffixContext *ctx);

    antlrcpp::Any visitData_type(SystemRDLParser::Data_typeContext *ctx);

    antlrcpp::Any visitBasic_data_type(SystemRDLParser::Basic_data_typeContext *ctx);

    antlrcpp::Any visitLiteral(SystemRDLParser::LiteralContext *ctx);

    antlrcpp::Any visitNumberHex(SystemRDLParser::NumberHexContext *ctx);

    antlrcpp::Any visitNumberVerilog(SystemRDLParser::NumberVerilogContext *ctx);

    antlrcpp::Any visitNumberInt(SystemRDLParser::NumberIntContext *ctx);

    antlrcpp::Any visitString_literal(SystemRDLParser::String_literalContext *ctx);

    antlrcpp::Any visitBoolean_literal(SystemRDLParser::Boolean_literalContext *ctx);

    antlrcpp::Any visitArray_literal(SystemRDLParser::Array_literalContext *ctx);

    antlrcpp::Any visitStruct_literal(SystemRDLParser::Struct_literalContext *ctx);

    antlrcpp::Any visitStruct_kv(SystemRDLParser::Struct_kvContext *ctx);

    antlrcpp::Any visitEnum_literal(SystemRDLParser::Enum_literalContext *ctx);

    antlrcpp::Any visitAccesstype_literal(SystemRDLParser::Accesstype_literalContext *ctx);

    antlrcpp::Any visitOnreadtype_literal(SystemRDLParser::Onreadtype_literalContext *ctx);

    antlrcpp::Any visitOnwritetype_literal(SystemRDLParser::Onwritetype_literalContext *ctx);

    antlrcpp::Any visitAddressingtype_literal(SystemRDLParser::Addressingtype_literalContext *ctx);

    antlrcpp::Any visitPrecedencetype_literal(SystemRDLParser::Precedencetype_literalContext *ctx);

    antlrcpp::Any visitInstance_ref(SystemRDLParser::Instance_refContext *ctx);

    antlrcpp::Any visitInstance_ref_element(SystemRDLParser::Instance_ref_elementContext *ctx);

    antlrcpp::Any visitProp_ref(SystemRDLParser::Prop_refContext *ctx);

    antlrcpp::Any visitLocal_property_assignment(SystemRDLParser::Local_property_assignmentContext *ctx);

    antlrcpp::Any visitDynamic_property_assignment(SystemRDLParser::Dynamic_property_assignmentContext *ctx);

    antlrcpp::Any visitNormal_prop_assign(SystemRDLParser::Normal_prop_assignContext *ctx);

    antlrcpp::Any visitEncode_prop_assign(SystemRDLParser::Encode_prop_assignContext *ctx);

    antlrcpp::Any visitProp_mod_assign(SystemRDLParser::Prop_mod_assignContext *ctx);

    antlrcpp::Any visitProp_assignment_rhs(SystemRDLParser::Prop_assignment_rhsContext *ctx);

    antlrcpp::Any visitProp_keyword(SystemRDLParser::Prop_keywordContext *ctx);

    antlrcpp::Any visitProp_mod(SystemRDLParser::Prop_modContext *ctx);

    antlrcpp::Any visitUdp_def(SystemRDLParser::Udp_defContext *ctx);

    antlrcpp::Any visitUdp_attr(SystemRDLParser::Udp_attrContext *ctx);

    antlrcpp::Any visitUdp_type(SystemRDLParser::Udp_typeContext *ctx);

    antlrcpp::Any visitUdp_data_type(SystemRDLParser::Udp_data_typeContext *ctx);

    antlrcpp::Any visitUdp_usage(SystemRDLParser::Udp_usageContext *ctx);

    antlrcpp::Any visitUdp_comp_type(SystemRDLParser::Udp_comp_typeContext *ctx);

    antlrcpp::Any visitUdp_default(SystemRDLParser::Udp_defaultContext *ctx);

    antlrcpp::Any visitUdp_constraint(SystemRDLParser::Udp_constraintContext *ctx);

    antlrcpp::Any visitEnum_def(SystemRDLParser::Enum_defContext *ctx);

    antlrcpp::Any visitEnum_entry(SystemRDLParser::Enum_entryContext *ctx);

    antlrcpp::Any visitEnum_prop_assign(SystemRDLParser::Enum_prop_assignContext *ctx);

    antlrcpp::Any visitStruct_def(SystemRDLParser::Struct_defContext *ctx);

    antlrcpp::Any visitStruct_elem(SystemRDLParser::Struct_elemContext *ctx);

    antlrcpp::Any visitStruct_type(SystemRDLParser::Struct_typeContext *ctx);

    antlrcpp::Any visitConstraint_def(SystemRDLParser::Constraint_defContext *ctx);

    antlrcpp::Any visitConstraint_named_def(SystemRDLParser::Constraint_named_defContext *ctx);

    antlrcpp::Any visitConstraint_anon_def(SystemRDLParser::Constraint_anon_defContext *ctx);

    antlrcpp::Any visitConstraint_body(SystemRDLParser::Constraint_bodyContext *ctx);

    antlrcpp::Any visitConstraint_body_elem(SystemRDLParser::Constraint_body_elemContext *ctx);

    antlrcpp::Any visitConstraint_insts(SystemRDLParser::Constraint_instsContext *ctx);

    antlrcpp::Any visitConstr_relational(SystemRDLParser::Constr_relationalContext *ctx);

    antlrcpp::Any visitConstr_prop_assign(SystemRDLParser::Constr_prop_assignContext *ctx);

    antlrcpp::Any visitConstr_inside_values(SystemRDLParser::Constr_inside_valuesContext *ctx);

    antlrcpp::Any visitConstr_inside_enum(SystemRDLParser::Constr_inside_enumContext *ctx);

    antlrcpp::Any visitConstr_lhs(SystemRDLParser::Constr_lhsContext *ctx);

    antlrcpp::Any visitConstr_inside_value(SystemRDLParser::Constr_inside_valueContext *ctx);

};