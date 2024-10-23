"""
Test cases for sequential signature
"""
from structmsig.sequential_struct import sign, verify
from structmsig.utils import create_struct_data

S1_PRIKEY = 'tests/s1-priv.pem'
S1_CERT = 'tests/s1-cert.pem'
S2_PRIKEY = 'tests/s2-priv.pem'
S2_CERT = 'tests/s2-cert.pem'

data = create_struct_data(
    texts={'text1':'Hello', 'text2':'World'}, files={'file1':'tests/data'}
)

def test_seqsig_all_success():
    """Success case for signing all data items"""
    seq_sig = sign('Signer1', data, S1_PRIKEY)
    seq_sig = sign('Signer2', data, S2_PRIKEY, seq_sig=seq_sig)
    result = verify(data, seq_sig, [S1_CERT, S2_CERT])
    assert result is True

def test_seqsig_all_fail_by_cert():
    """Fail case for signing all data items because of wrong certificate"""
    seq_sig = sign('Signer1', data, S1_PRIKEY)
    seq_sig = sign('Signer2', data, S2_PRIKEY, seq_sig=seq_sig)
    result = verify(data, seq_sig, [S2_CERT, S1_CERT])
    assert result is False

def test_nodalsig_all_fail_by_scope():
    """Fail case for signing all data items because of wrong scope"""
    seq_sig = sign('Signer1', data, S1_PRIKEY)
    seq_sig = sign('Signer2', data, S2_PRIKEY, seq_sig=seq_sig)
    seq_sig.signatures[1].scope = ['file1']
    result = verify(data, seq_sig, [S1_CERT, S2_CERT])
    assert result is False

def test_seqsig_portion_success():
    """Success case for signing data with scope specified by signers"""
    seq_sig = sign('Signer1', data, S1_PRIKEY, scope=['file1','text1'])
    seq_sig = sign('Signer2', data, S2_PRIKEY, scope=['file1'], seq_sig=seq_sig)
    result = verify(data, seq_sig, [S1_CERT, S2_CERT])
    assert result is True

def test_seqsig_portion_fail_by_cert():
    """Fail case for signing data with scope specified by signers because of wrong certificate"""
    seq_sig = sign('Signer1', data, S1_PRIKEY, scope=['file1','text1'])
    seq_sig = sign('Signer2', data, S2_PRIKEY, scope=['file1'], seq_sig=seq_sig)
    result = verify(data, seq_sig, [S2_CERT, S1_CERT])
    assert result is False

def test_seqsig_portion_fail_by_scope():
    """Fail case for signing data with scope specified by signers because of wrong scope"""
    seq_sig = sign('Signer1', data, S1_PRIKEY, scope=['file1','text1'])
    seq_sig = sign('Signer2', data, S2_PRIKEY, scope=['file1'], seq_sig=seq_sig)
    seq_sig.signatures[1].scope = ['text2']
    result = verify(data, seq_sig, [S1_CERT, S2_CERT])
    assert result is False