"""
Test cases for node signature
"""
from structmsig.nodal_struct import sign, verify
from structmsig.utils import create_struct_data

S1_PRIKEY = 'tests/s1-priv.pem'
S1_CERT = 'tests/s1-cert.pem'
S2_CERT = 'tests/s2-cert.pem'

data = create_struct_data(
    texts={'text1':'Hello', 'text2':'World'}, files={'file1':'tests/data'}
)

def test_nodalsig_all_success():
    """Success case for signing all data items"""
    nodal_sig = sign('Signer1', data, S1_PRIKEY)
    result = verify(data, nodal_sig, S1_CERT)
    assert result is True

def test_nodalsig_all_fail_by_cert():
    """Fail case for signing all data items because of wrong certificate"""
    nodal_sig = sign('Signer1', data, S1_PRIKEY)
    result = verify(data, nodal_sig, S2_CERT)
    assert result is False

def test_nodalsig_all_fail_by_scope():
    """Fail case for signing all data items because of wrong scope"""
    nodal_sig = sign('Signer1', data, S1_PRIKEY)
    nodal_sig.scope = ['text1', 'file1']
    result = verify(data, nodal_sig, S2_CERT)
    assert result is False

def test_nodalsig_portion_success():
    """Success case for signing data with scope specified by signer"""
    nodal_sig = sign('Signer1', data, S1_PRIKEY, scope=['file1','text1'])
    result = verify(data, nodal_sig, S1_CERT)
    assert result is True

def test_nodalsig_portion_fail_by_cert():
    """Fail case for signing data with scope specified by signer because of wrong certificate"""
    nodal_sig = sign('Signer1', data, S1_PRIKEY, scope=['file1','text1'])
    result = verify(data, nodal_sig, S2_CERT)
    assert result is False

def test_nodalsig_portion_fail_by_scope():
    """Fail case for signing data with scope specified by signer because of wrong scope"""
    nodal_sig = sign('Signer1', data, S1_PRIKEY, scope=['file1','text1'])
    nodal_sig.scope = ['file1']
    result = verify(data, nodal_sig, S1_CERT)
    assert result is False