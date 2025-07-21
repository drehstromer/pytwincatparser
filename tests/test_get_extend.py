from pytwincatparser.parse_declaration import get_extend

def test_get_extend():
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface""") == ["FB_SubBase", "FB_SubSubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase""") == ["FB_SubBase", "FB_SubSubBase"]
    assert get_extend("""extends FB_SubBase, FB_SubSubBase""") == ["FB_SubBase", "FB_SubSubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED""") == None
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED (* extends this and that *)""") == None
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED (* extends this and that *) EXTENDS FB_SubBase""") == ["FB_SubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED // extends this and that """) == None
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED // extends this and that EXTENDS """) == None
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED EXTENDS FB_SubBase""") == ["FB_SubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED IMPLEMENTS I_Elementinformation, I_TestInterface EXTENDS FB_SubBase""") == ["FB_SubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base PROTECTED EXTENDS FB_SubBase implements I_AnotherTestInterface""") == ["FB_SubBase"]
    assert get_extend("""INTERFACE I_Data Extends __System.IQueryInterface""") == ["__System.IQueryInterface"]
    assert get_extend("""FUNCTION_BLOCK FB_UtilitiesModuleControl EXTENDS FB_Base
(*details Controls and checks all supplies, e.g. Power and Pneumatic *)""") == ["FB_Base"]
    assert get_extend("""FUNCTION_BLOCK FB_ProvidePmlCommand EXTENDS FB_Provide
(*details Functionblock to provide PmlCommands. The counterpart of this FB is the [FB_PullPmlCommand][LCA_NGP_Core.FB_PullPmlCommand].*)

VAR
	_stPmlCommand : ST_PmlCommand;
END_VAR""") == ["FB_Provide"]