import shutil
import tempfile
import os

from electrum.storage import WalletStorage
from electrum.wallet import Wallet
from electrum import constants

from .test_wallet import WalletTestCase


# TODO add other wallet types: 2fa, xpub-only
# TODO hw wallet with client version 2.6.x (single-, and multiacc)
class TestStorageUpgrade(WalletTestCase):

    def testnet_wallet(func):
        # note: it's ok to modify global network constants in subclasses of SequentialTestCase
        def wrapper(self, *args, **kwargs):
            constants.set_testnet()
            try:
                return func(self, *args, **kwargs)
            finally:
                constants.set_mainnet()
        return wrapper

    def test_upgrade_from_client_3_2_2_seeded(self):
        wallet_str = '{"addr_history":{"jzx3JSH5goW4BzBrZx6jzc33CTuGFWPhZHG":[],"jzy4jRnRyipLJjmKUohA9LfBxgY5Cckjrt6":[],"jzyYwo4h4DDPciPDHK9HRW8nLGBhCSmuTUC":[],"jzz7ykr7BF2uwMwQuwPYF62VgMTUgkx4UnV":[],"jzzantXiovyUcYRMYBcTDQTdRrbT4EeRLii":[],"k11JBnsANuSZwitcz249zKHhLbphdivKSkv":[],"k11XHvyz9mFpVPPfYzijNtaLePpNB5drJ2Z":[],"k125oeKN6W1wWgap8dRaGPipiYaDbNNMcLx":[],"k14dqjy5peppbGfto1xbVTbD8k9KYEvZ58x":[],"k15XuMUBEcZevDYSxHwgmVw9XcMEKZmKLN4":[],"k15cg8HPrMuMh79mz5UeZmxYveZ5QAYUKsx":[],"k16Qfsb6uH8FsRf6eKnA22CPDFUiwPLWNRm":[],"k16paU3g1TjiXesH3JFdYRABFurHeJoYVqm":[],"k16t4BoN134gtcNv3fuLCosBQTgRqcB39YC":[],"k1AkMSij9D7NVSCnrRnAzcktniZ2jBinkQd":[],"k1AuWRToySeNXjqgUyUGEJb2PnURzAxJGeA":[],"k1DHkBmCAEHy5QdL6xewAzHNLEiVKkHjZne":[],"k1DMNRquMo3VKtLNboBe8sXxSTwFJqP7cWc":[],"k1DYJZyH6sDfLD8nmr5jh758gGVFxDTDch1":[],"k1EuzCVqzL5hC4cMrnbBEB8E4xnNP1T4rEU":[],"k1FMWC2BevqujHvdYXmzdT3QP6ehBYwuih7":[],"k1GEpheQi2cKfLoSFBAk5NL9fHrQ8uuabi2":[],"k1GeVJh3gx1jJmBR9fEGvKiFH6dySMEeMkZ":[],"k1Gg1yQyJSjbR546oFtffHyA76ZcQ1bV9QQ":[],"k1JqdiEtDGF96ucC8VnEqhSxLahM8SGxSBu":[],"k1Lbf3D9f6SGLUrZFZ4E9M8FunbhE1qSdMs":[]},"addresses":{"change":["k1DYJZyH6sDfLD8nmr5jh758gGVFxDTDch1","k1DHkBmCAEHy5QdL6xewAzHNLEiVKkHjZne","k125oeKN6W1wWgap8dRaGPipiYaDbNNMcLx","k16t4BoN134gtcNv3fuLCosBQTgRqcB39YC","k16paU3g1TjiXesH3JFdYRABFurHeJoYVqm","k1FMWC2BevqujHvdYXmzdT3QP6ehBYwuih7"],"receiving":["k11XHvyz9mFpVPPfYzijNtaLePpNB5drJ2Z","jzz7ykr7BF2uwMwQuwPYF62VgMTUgkx4UnV","k16Qfsb6uH8FsRf6eKnA22CPDFUiwPLWNRm","k1EuzCVqzL5hC4cMrnbBEB8E4xnNP1T4rEU","k1Lbf3D9f6SGLUrZFZ4E9M8FunbhE1qSdMs","jzzantXiovyUcYRMYBcTDQTdRrbT4EeRLii","k1GEpheQi2cKfLoSFBAk5NL9fHrQ8uuabi2","jzy4jRnRyipLJjmKUohA9LfBxgY5Cckjrt6","jzyYwo4h4DDPciPDHK9HRW8nLGBhCSmuTUC","k11JBnsANuSZwitcz249zKHhLbphdivKSkv","k1Gg1yQyJSjbR546oFtffHyA76ZcQ1bV9QQ","k14dqjy5peppbGfto1xbVTbD8k9KYEvZ58x","k1AuWRToySeNXjqgUyUGEJb2PnURzAxJGeA","k15XuMUBEcZevDYSxHwgmVw9XcMEKZmKLN4","k1GeVJh3gx1jJmBR9fEGvKiFH6dySMEeMkZ","k15cg8HPrMuMh79mz5UeZmxYveZ5QAYUKsx","jzx3JSH5goW4BzBrZx6jzc33CTuGFWPhZHG","k1AkMSij9D7NVSCnrRnAzcktniZ2jBinkQd","k1DMNRquMo3VKtLNboBe8sXxSTwFJqP7cWc","k1JqdiEtDGF96ucC8VnEqhSxLahM8SGxSBu"]},"keystore":{"seed":"cereal wise two govern top pet frog nut rule sketch bundle logic","type":"bip32","xprv":"xprv9s21ZrQH143K29XjRjUs6MnDB9wXjXbJP2kG1fnRk8zjdDYWqVkQYUqaDtgZp5zPSrH5PZQJs8sU25HrUgT1WdgsPU8GbifKurtMYg37d4v","xpub":"xpub661MyMwAqRbcEdcCXm1sTViwjBn28zK9kFfrp4C3JUXiW1sfP34f6HA45B9yr7EH5XGzWuTfMTdqpt9XPrVQVUdgiYb5NW9m8ij1FSZgGBF"},"seed_type":"standard","seed_version":18,"spent_outpoints":{},"stored_height":522210,"transactions":{},"tx_fees":{},"txi":{},"txo":{},"use_encryption":false,"verified_tx3":{},"wallet_type":"standard","winpos-qt":[823,202,840,400]}'
        self._upgrade_storage(wallet_str)

    def test_upgrade_from_client_3_2_2_importedkeys(self):
        wallet_str = '{"addr_history":{"jzyvb3tU9tE8gmsngH6PW7NtgL7tAo13fq1":[],"k123VxhnLHSuoWs1dKGF8nQ4jj25nVYfJBL":[],"k1BoBd3dMv1JT9v6dUx5CiUkSUs9TF1Dzi7":[]},"addresses":{"jzyvb3tU9tE8gmsngH6PW7NtgL7tAo13fq1":{"pubkey":"0344b1588589958b0bcab03435061539e9bcf54677c104904044e4f8901f4ebdf5","redeem_script":null,"type":"p2pkh"},"k123VxhnLHSuoWs1dKGF8nQ4jj25nVYfJBL":{"pubkey":"04575f52b82f159fa649d2a4c353eb7435f30206f0a6cb9674fbd659f45082c37d559ffd19bea9c0d3b7dcc07a7b79f4cffb76026d5d4dff35341efe99056e22d2","redeem_script":null,"type":"p2pkh"},"k1BoBd3dMv1JT9v6dUx5CiUkSUs9TF1Dzi7":{"pubkey":"0389508c13999d08ffae0f434a085f4185922d64765c0bff2f66e36ad7f745cc5f","redeem_script":null,"type":"p2pkh"}},"keystore":{"keypairs":{"0344b1588589958b0bcab03435061539e9bcf54677c104904044e4f8901f4ebdf5":"L2sED74axVXC4H8szBJ4rQJrkfem7UMc6usLCPUoEWxDCFGUaGUM","0389508c13999d08ffae0f434a085f4185922d64765c0bff2f66e36ad7f745cc5f":"L3Gi6EQLvYw8gEEUckmqawkevfj9s8hxoQDFveQJGZHTfyWnbk1U","04575f52b82f159fa649d2a4c353eb7435f30206f0a6cb9674fbd659f45082c37d559ffd19bea9c0d3b7dcc07a7b79f4cffb76026d5d4dff35341efe99056e22d2":"5JyVyXU1LiRXATvRTQvR9Kp8Rx1X84j2x49iGkjSsXipydtByUq"},"type":"imported"},"seed_version":18,"spent_outpoints":{},"transactions":{},"tx_fees":{},"txi":{},"txo":{},"use_encryption":false,"verified_tx3":{},"wallet_type":"imported"}'

    def test_upgrade_from_client_3_2_2_watchaddresses(self):
        wallet_str = '{"addr_history":{"k15SSr9dJETnjuj97mZJA2EQFiY8ss67JvL":[],"k1DKzMLXyGZfcX5rYiUT5XMBMwfefiYR7No":[],"k1DNUhxZnQudZNDE4zU3xwbwKza3tkyro2w":[]},"addresses":{"k15SSr9dJETnjuj97mZJA2EQFiY8ss67JvL":{},"k1DKzMLXyGZfcX5rYiUT5XMBMwfefiYR7No":{},"k1DNUhxZnQudZNDE4zU3xwbwKza3tkyro2w":{}},"seed_version":18,"spent_outpoints":{},"transactions":{},"tx_fees":{},"txi":{},"txo":{},"wallet_type":"imported"}'
        self._upgrade_storage(wallet_str)

    def test_upgrade_from_client_3_2_2_trezor_singleacc(self):
        wallet_str = '''{"addr_history":{"jzxSNKonMV1mHPKphkM4ZSs4tJECbUQp9vR":[],"jzxfX5XQHfZeJsLu1KmJPSaGiLcxKBv5gXe":[],"jzy9H451o6jGP5ydmjKFAUdmw9WK4BoyV3H":[],"jzzGSvvxLS2qjtB5Xr4VosftWw1M3vjZVcL":[],"jzzHMTbASBhNni9jUDoKMd15g1BZ8qrjyo8":[],"k11VJQnVbGEjnFdYSsrynt73WFhNsEwSxNc":[],"k12YphgF9xvgqwxPrsFir7KSSYfB4ZyDtuv":[],"k13LeBQSs2ohmA5AgyPAGrRZnKdVC3XMKr9":[],"k149kdKmj5F3hX9zPhN13g6kEVxqrNW5tAD":[],"k14Xt2nnCSKP4NL65EtXAdj9E43d2wpFXd9":[],"k157BZ51ZoVbvu5M1P4Pb5ncoTJsUsoeXod":[],"k17GujToMGQXK6aAYRAkNu2EN4VWodhLWyQ":[],"k18uGUUDwYwhtitmtb6vsCnBTCHC1GKWsdm":[],"k1CY378KfCNcf47LTnN24eYMt5triDRLNss":[],"k1DUFmNzi4U46eYEHFGnZavNrp1oCzWgNK6":[],"k1Dikugq7J54RmZxG9pHs5n385xLqXPHXUv":[],"k1EwY3rCCNqPDXSVDNUfCdUG7yY1eUe6cp8":[],"k1FwkDDDVEyiNZJc7WbsKsjSRbVVsDSdMjx":[],"k1HC6iYmoWJ84qidBB7mzVuGuMR87uSodYJ":[],"k1HLNxF6L2YG62qctKhGt6LkPgg515yYD1b":[],"k1J4JeLcDZEvHEg61ccnsXoe6vEgwSyanLB":[],"k1Ji61LzLvMS4cXdETUyvQahkmcGFbadJzA":[],"k1K7Fg4Vj9SkWAwXf2GQGDGZJb6S5qSUcLs":[],"k1Kf4JUAAbuJp5kw9KxvbRE8Lvio7Gfd2A6":[],"k1LXRPsLvgxezhKg8bnb5JzYQiA1gLzK3Mw":[],"k1LmSZjqiyJhKzdxMmtLGJYgVrm6zANtemW":[]},"addresses":{"change":["k1HC6iYmoWJ84qidBB7mzVuGuMR87uSodYJ","k12YphgF9xvgqwxPrsFir7KSSYfB4ZyDtuv","k1Ji61LzLvMS4cXdETUyvQahkmcGFbadJzA","k1CY378KfCNcf47LTnN24eYMt5triDRLNss","k1J4JeLcDZEvHEg61ccnsXoe6vEgwSyanLB","k17GujToMGQXK6aAYRAkNu2EN4VWodhLWyQ"],"receiving":["k11VJQnVbGEjnFdYSsrynt73WFhNsEwSxNc","k1Dikugq7J54RmZxG9pHs5n385xLqXPHXUv","jzxfX5XQHfZeJsLu1KmJPSaGiLcxKBv5gXe","k1FwkDDDVEyiNZJc7WbsKsjSRbVVsDSdMjx","k13LeBQSs2ohmA5AgyPAGrRZnKdVC3XMKr9","jzzGSvvxLS2qjtB5Xr4VosftWw1M3vjZVcL","k1Kf4JUAAbuJp5kw9KxvbRE8Lvio7Gfd2A6","k1LXRPsLvgxezhKg8bnb5JzYQiA1gLzK3Mw","k18uGUUDwYwhtitmtb6vsCnBTCHC1GKWsdm","k1K7Fg4Vj9SkWAwXf2GQGDGZJb6S5qSUcLs","jzzHMTbASBhNni9jUDoKMd15g1BZ8qrjyo8","k1LmSZjqiyJhKzdxMmtLGJYgVrm6zANtemW","jzxSNKonMV1mHPKphkM4ZSs4tJECbUQp9vR","k1DUFmNzi4U46eYEHFGnZavNrp1oCzWgNK6","k1EwY3rCCNqPDXSVDNUfCdUG7yY1eUe6cp8","k14Xt2nnCSKP4NL65EtXAdj9E43d2wpFXd9","k149kdKmj5F3hX9zPhN13g6kEVxqrNW5tAD","jzy9H451o6jGP5ydmjKFAUdmw9WK4BoyV3H","k1HLNxF6L2YG62qctKhGt6LkPgg515yYD1b","k157BZ51ZoVbvu5M1P4Pb5ncoTJsUsoeXod"]},"keystore":{"derivation":"m/44'/510'/0'","hw_type":"trezor","label":null,"type":"hardware","xpub":"xpub6CfeMiz99uDXtm5yrsSMX6wtYVrKw5FYt7UvTZPmCLjXD5XFNW8df8YXNvpdmfLaWHiwvMjmFSMkXMUG6kQ4AoLPcWhQmvpay9PLbg1Xvwe"},"seed_version":18,"spent_outpoints":{},"stored_height":522238,"transactions":{},"tx_fees":{},"txi":{},"txo":{},"use_encryption":false,"verified_tx3":{},"wallet_type":"standard","winpos-qt":[100,100,840,400]}'''
        self._upgrade_storage(wallet_str)

    def test_upgrade_from_client_3_2_2_multisig(self):
        wallet_str = '{"addr_history":{"k2xkFaM9bgXSwc1fhu3HABp6pjhzhLm1fcP":[],"k2yDiUmySZZqjFLHCsr3VmbbRt7ATTHWhon":[],"k2z5w6EXmhUPvB1NGEckSwc6WJ52YLLsFVB":[],"k2zBvytY7pq1FzkrVckfs5y6j9H7Ka9Jk1x":[],"k2zmSStUBRzC2b371oC3ZHzcSYzyJo32QjH":[],"k32j86uTVoQpTusXYZuhtqosAU2UBRbmv5Y":[],"k33qE2GKvnB5sZjTZeUo55DDPazuNJWVekA":[],"k34h6eVKPGTYKFz2de8yUP3FEideAR7MBZu":[],"k34zZ4EyD3uTpPsa7xy2LPr1CeYuGauEHio":[],"k357626iNaUNCvKx4s31SLyY5AkSHJDSJ5z":[],"k375RhsecLgxaNXMMTaDM9Cncj1upDfHkd3":[],"k37QpFrJCdW2Pp95LBVn9dq66agfbZgcAnF":[],"k39zjkB8x9WzfW1t8am2rGgW1sYYUiRR7Yg":[],"k3D9awD3Ma3pJUsJsebBBYXnij5Znrk4orK":[],"k3DqfhoCe9BZfRXWsbuGfMMhWjDvNMnzozW":[],"k3FYHKnMwo7JRkCSyKG1qDqydnGQuBowtY2":[],"k3FigoySpwe6gFXh5vvmkcL183uVfJH9X2x":[],"k3GFLcghuu1XHZRzoQufN5BC2xVwEuNdPiV":[],"k3GNAm1U1Ht4XpnFcNgjgMQZiYgVrHVarM1":[],"k3GQEyQAj7Rfyp555AWLCbvjYNQSt4Rn9zf":[],"k3GUz4JkGNhQWEwur24imNfDbKeM4KeAfL5":[],"k3Gv7JMKswafavPYG3iF8v1WLgrVbj3LwFp":[],"k3GzvamHAgL4wUbSJgzv2uhJTNay3LZi4KY":[],"k3Ksq3RFdzPxNiN8tSW385mvbfHx48p5DPE":[],"k3LWuNNz7CXUUcKuXfQZQkoKrQB2YJtMe1q":[],"k3LbdxbvfCMQToUvRmoRdM8sH6EN2bQ72Y1":[]},"addresses":{"change":["k2xkFaM9bgXSwc1fhu3HABp6pjhzhLm1fcP","k3FYHKnMwo7JRkCSyKG1qDqydnGQuBowtY2","k3D9awD3Ma3pJUsJsebBBYXnij5Znrk4orK","k3GzvamHAgL4wUbSJgzv2uhJTNay3LZi4KY","k2zBvytY7pq1FzkrVckfs5y6j9H7Ka9Jk1x","k375RhsecLgxaNXMMTaDM9Cncj1upDfHkd3"],"receiving":["k3Ksq3RFdzPxNiN8tSW385mvbfHx48p5DPE","k2z5w6EXmhUPvB1NGEckSwc6WJ52YLLsFVB","k39zjkB8x9WzfW1t8am2rGgW1sYYUiRR7Yg","k37QpFrJCdW2Pp95LBVn9dq66agfbZgcAnF","k3DqfhoCe9BZfRXWsbuGfMMhWjDvNMnzozW","k33qE2GKvnB5sZjTZeUo55DDPazuNJWVekA","k34h6eVKPGTYKFz2de8yUP3FEideAR7MBZu","k34zZ4EyD3uTpPsa7xy2LPr1CeYuGauEHio","k357626iNaUNCvKx4s31SLyY5AkSHJDSJ5z","k2zmSStUBRzC2b371oC3ZHzcSYzyJo32QjH","k3Gv7JMKswafavPYG3iF8v1WLgrVbj3LwFp","k3GNAm1U1Ht4XpnFcNgjgMQZiYgVrHVarM1","k3GFLcghuu1XHZRzoQufN5BC2xVwEuNdPiV","k3GQEyQAj7Rfyp555AWLCbvjYNQSt4Rn9zf","k2yDiUmySZZqjFLHCsr3VmbbRt7ATTHWhon","k3GUz4JkGNhQWEwur24imNfDbKeM4KeAfL5","k3FigoySpwe6gFXh5vvmkcL183uVfJH9X2x","k3LWuNNz7CXUUcKuXfQZQkoKrQB2YJtMe1q","k3LbdxbvfCMQToUvRmoRdM8sH6EN2bQ72Y1","k32j86uTVoQpTusXYZuhtqosAU2UBRbmv5Y"]},"seed_version":18,"spent_outpoints":{},"transactions":{},"tx_fees":{},"txi":{},"txo":{},"use_encryption":false,"verified_tx3":{},"wallet_type":"2of2","x1/":{"seed":"speed cruise market wasp ability alarm hold essay grass coconut tissue recipe","type":"bip32","xprv":"xprv9s21ZrQH143K48ig2wcAuZoEKaYdNRaShKFR3hLrgwsNW13QYRhXH6gAG1khxim6dw2RtAzF8RWbQxr1vvWUJFfEu2SJZhYbv6pfreMpuLB","xpub":"xpub661MyMwAqRbcGco98y9BGhjxscP7mtJJ4YB1r5kUFHQMNoNZ5y1mptze7J37JypkbrmBdnqTvSNzxL7cE1FrHg16qoj9S12MUpiYxVbTKQV"},"x2/":{"type":"bip32","xprv":null,"xpub":"xpub661MyMwAqRbcGrCDZaVs9VC7Z6579tsGvpqyDYZEHKg2MXoDkxhrWoukqvwDPXKdxVkYA6Hv9XHLETptfZfNpcJZmsUThdXXkTNGoBjQv1o"}}'
        self._upgrade_storage(wallet_str)

##########

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from electrum.plugin import Plugins
        from electrum.simple_config import SimpleConfig

        cls.__electrum_path = tempfile.mkdtemp()
        config = SimpleConfig({'electrum_path': cls.__electrum_path})

        gui_name = 'cmdline'
        # TODO it's probably wasteful to load all plugins... only need Trezor
        Plugins(config, gui_name)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(cls.__electrum_path)

    def _upgrade_storage(self, wallet_json, accounts=1):
        if accounts == 1:
            # test manual upgrades
            storage = self._load_storage_from_json_string(wallet_json=wallet_json,
                                                          path=self.wallet_path,
                                                          manual_upgrades=True)
            self.assertFalse(storage.requires_split())
            if storage.requires_upgrade():
                storage.upgrade()
                self._sanity_check_upgraded_storage(storage)
            # test automatic upgrades
            path2 = os.path.join(self.user_dir, "somewallet2")
            storage2 = self._load_storage_from_json_string(wallet_json=wallet_json,
                                                           path=path2,
                                                           manual_upgrades=False)
            storage2.write()
            self._sanity_check_upgraded_storage(storage2)
            # test opening upgraded storages again
            s1 = WalletStorage(path2, manual_upgrades=False)
            self._sanity_check_upgraded_storage(s1)
            s2 = WalletStorage(path2, manual_upgrades=True)
            self._sanity_check_upgraded_storage(s2)
        else:
            storage = self._load_storage_from_json_string(wallet_json=wallet_json,
                                                          path=self.wallet_path,
                                                          manual_upgrades=True)
            self.assertTrue(storage.requires_split())
            new_paths = storage.split_accounts()
            self.assertEqual(accounts, len(new_paths))
            for new_path in new_paths:
                new_storage = WalletStorage(new_path, manual_upgrades=False)
                self._sanity_check_upgraded_storage(new_storage)

    def _sanity_check_upgraded_storage(self, storage):
        self.assertFalse(storage.requires_split())
        self.assertFalse(storage.requires_upgrade())
        w = Wallet(storage, config=self.config)

    @staticmethod
    def _load_storage_from_json_string(*, wallet_json, path, manual_upgrades):
        with open(path, "w") as f:
            f.write(wallet_json)
        storage = WalletStorage(path, manual_upgrades=manual_upgrades)
        return storage
