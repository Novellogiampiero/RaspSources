MCUX_WORKSPACE_LOC=/home/novello/nfc/reader
MCUX_FLASH_DIR0=/usr/local/mcuxpressoide-11.1.1_3241/ide/plugins/com.nxp.mcuxpresso.tools.bin.linux_11.1.0.202002241259/binaries/Flash
MCUX_IDE_BIN=/usr/local/mcuxpressoide-11.1.1_3241/ide/plugins/com.nxp.mcuxpresso.tools.bin.linux_11.1.0.202002241259/binaries/
$MCUX_IDE_BIN/crt_emu_cm_redlink --flash-load-exec "$MCUX_WORKSPACE_LOC/NfcrdlibEx3_NFCForum/ReleasePN7462AU/NfcrdlibEx3_NFCForum.axf" -p PN7462AU-C3-00 --ConnectScript PN7xxxxx_Connect.scp --flash-driver PN7xxxxx_158k.cfx --flash-hashing
MCUX_WORKSPACE_LOC=/home/novello/nfc/reader
MCUX_FLASH_DIR0=/usr/local/mcuxpressoide-11.1.1_3241/ide/plugins/com.nxp.mcuxpresso.tools.bin.linux_11.1.0.202002241259/binaries/Flash
MCUX_IDE_BIN=/usr/local/mcuxpressoide-11.1.1_3241/ide/plugins/com.nxp.mcuxpresso.tools.bin.linux_11.1.0.202002241259/binaries/
$MCUX_IDE_BIN/crt_emu_cm_redlink --flash-load-exec "$MCUX_WORKSPACE_LOC/PN7462AU/phHal/phCfg/xml/user_ee.bin" -p PN7462AU-C3-00 --load-base=0x201200 --ConnectScript PN7xxxxx_Connect.scp --flash-driver PN7xxxxx_EE_3_5k.cfx --flash-hashing
