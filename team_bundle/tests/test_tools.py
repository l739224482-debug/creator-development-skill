import unittest,json,tempfile,sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from credentials import encrypt,decrypt
from nox import perform,sanitize,plan
from metrics import calculate
class Tools(unittest.TestCase):
    def state(self,path,budget=5):
        (path/'state.json').write_text(json.dumps({'task_id':'fixture','budget':budget,'consumed':0,'calls':[],'blocked':False}))
    def test_cipher_roundtrip_and_wrong_password(self):
        keys=['nox_FAKE_TEST_SECRET_1234567890','nox_FAKE_2'];p=encrypt(keys,'fixture-password')
        self.assertEqual(decrypt(p,'fixture-password'),keys)
        self.assertNotIn(keys[0],json.dumps(p))
        with self.assertRaises(Exception):decrypt(p,'wrong-password')
    def test_mean_is_not_every_video_and_zero_is_known(self):
        vs=[{'id':str(i),'timestamp':i,'views':v,'likes':1000,'comments':0,'is_pinned':False}for i,v in enumerate([1,1000,11000,12000,13000,14000,15000,16000,17000,18000,19000,1000000])]
        self.assertTrue(calculate(vs,10000,.01)['numeric_pass'])
        self.assertFalse(calculate(vs,10000,.01,9000)['numeric_pass'])
        vs[3]['likes']=None
        with self.assertRaises(ValueError):calculate(vs,10000,.01)
    def test_ties_remove_two_distinct_videos(self):
        vs=[{'id':str(i),'timestamp':i,'views':10001,'likes':200,'comments':0,'is_pinned':False}for i in range(12)]
        m=calculate(vs,10000,.01);self.assertEqual(len(m['retained_ids']),10);self.assertNotEqual(m['removed_low_id'],m['removed_high_id'])
    def test_no_network_when_budget_insufficient(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d);self.state(p,4.9)
            def runner(*a,**kw):self.fail('must not call provider')
            with self.assertRaises(RuntimeError):perform(p,['creator','profile','--','fixture-id'],runner=runner,key_loader=lambda:['fixture-secret'])
    def test_unknown_charge_blocks_and_no_retry(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d);self.state(p);calls=[]
            def runner(*a,**kw):calls.append(1);raise TimeoutError()
            for _ in range(2):
                with self.assertRaises(RuntimeError):perform(p,['creator','profile','--','fixture-id'],runner=runner,key_loader=lambda:['fixture-secret'])
            self.assertEqual(len(calls),1);self.assertTrue(json.loads((p/'state.json').read_text())['blocked'])
    def test_success_metered_and_key_redacted(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d);self.state(p)
            def runner(*a,**kw):return SimpleNamespace(stdout=json.dumps({'success':True,'credits':{'used':.2},'meta':{'request_id':'fixture-request'},'data':{'debug':'fixture-secret','api_key':'fixture-secret'}}))
            result=perform(p,['creator','profile','--','fixture-id'],runner=runner,key_loader=lambda:['fixture-secret'])
            self.assertEqual(json.loads((p/'state.json').read_text())['consumed'],.2);self.assertNotIn('fixture-secret',json.dumps(result));self.assertFalse(json.loads((p/'state.json').read_text())['blocked'])
    def test_no_mutation_or_global_credential_flags(self):
        for args in [['email','send'],['creator','contacts'],['creator','search','--api-key','fixture'],['creator','search','--page_size','101']]:
            with self.assertRaises(RuntimeError):plan(args)
if __name__=='__main__':unittest.main()
