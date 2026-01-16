import unittest
from unittest.mock import patch

import wifiip


class TestWifiip(unittest.TestCase):
    def test_mask_ip_ipv4(self):
        self.assertEqual(wifiip._mask_ip("192.168.1.55"), "192.168.1.x")

    def test_mask_ip_non_ipv4(self):
        self.assertEqual(wifiip._mask_ip("not-an-ip"), "x.x.x.x")

    def test_mask_mac(self):
        self.assertEqual(wifiip._mask_mac("aa:bb:cc:dd:ee:ff"), "aa:bb:cc:xx:xx:xx")

    def test_build_targets_prefix(self):
        targets = wifiip._build_targets("192.168.1")
        self.assertEqual(targets[0], "192.168.1.1")
        self.assertEqual(targets[-1], "192.168.1.254")
        self.assertEqual(len(targets), 254)

    def test_build_targets_cidr(self):
        targets = wifiip._build_targets("192.168.1.0/30")
        # /30 has 4 addresses, 2 usable hosts
        self.assertEqual(targets, ["192.168.1.1", "192.168.1.2"])

    def test_build_targets_rejects_large(self):
        with self.assertRaises(ValueError):
            wifiip._build_targets("10.0.0.0/8", max_hosts=100)

    @patch("wifiip.subprocess.run")
    @patch("wifiip.platform.system", return_value="Darwin")
    def test_read_arp_table_darwin(self, _system, run):
        class R:
            returncode = 0
            stdout = "? (192.168.1.1) at aa:bb:cc:dd:ee:ff on en0 ifscope [ethernet]\n"
            stderr = ""

        run.return_value = R()
        table = wifiip._read_arp_table()
        self.assertEqual(table["192.168.1.1"], "aa:bb:cc:dd:ee:ff")

    @patch("wifiip.subprocess.run")
    @patch("wifiip.platform.system", return_value="Windows")
    def test_read_arp_table_windows(self, _system, run):
        class R:
            returncode = 0
            stdout = (
                "Interface: 192.168.1.10 --- 0x7\n"
                "  Internet Address      Physical Address      Type\n"
                "  192.168.1.1          aa-bb-cc-dd-ee-ff     dynamic\n"
            )
            stderr = ""

        run.return_value = R()
        table = wifiip._read_arp_table()
        self.assertEqual(table["192.168.1.1"], "aa:bb:cc:dd:ee:ff")

    @patch("wifiip.subprocess.run")
    @patch("wifiip.platform.system", return_value="Linux")
    def test_read_arp_table_linux_ip_neigh(self, _system, run):
        class R:
            returncode = 0
            stdout = "192.168.1.1 dev wlan0 lladdr aa:bb:cc:dd:ee:ff REACHABLE\n"
            stderr = ""

        run.return_value = R()
        table = wifiip._read_arp_table()
        self.assertEqual(table["192.168.1.1"], "aa:bb:cc:dd:ee:ff")

    @patch("wifiip.subprocess.run")
    def test_ping_sweep_handles_missing_ping(self, run):
        def raise_fnf(*_args, **_kwargs):
            raise FileNotFoundError("ping")

        run.side_effect = raise_fnf
        with self.assertRaises(RuntimeError):
            wifiip.ping_sweep("192.168.1", workers=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
