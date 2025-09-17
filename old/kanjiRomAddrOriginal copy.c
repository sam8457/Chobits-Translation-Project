
undefined * kanjiRomAdrOriginal(undefined1 *param_1)

{
  byte bVar1;
  bool bVar2;
  undefined *puVar3;
  int iVar4;
  
  puVar3 = (undefined *)0x0;
  iVar4 = 0;
  bVar2 = false;
  switch(*param_1) {
  case 0x81:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] - 0x40;
    }
    break;
  case 0x82:
    bVar1 = param_1[1];
    if ((bVar1 < 0x4f) || (0xf1 < bVar1)) {
      bVar2 = true;
    }
    else {
      iVar4 = bVar1 + 0x71;
    }
    break;
  case 0x83:
    bVar1 = param_1[1];
    if ((bVar1 < 0x40) || (0xd6 < bVar1)) {
      bVar2 = true;
    }
    else {
      iVar4 = bVar1 + 0x123;
    }
    break;
  case 0x84:
    bVar1 = param_1[1];
    if ((bVar1 < 0x40) || (0xbe < bVar1)) {
      bVar2 = true;
    }
    else {
      iVar4 = bVar1 + 0x1ba;
    }
    break;
  default:
    bVar2 = true;
    break;
  case 0x87:
    bVar1 = param_1[1];
    if ((bVar1 < 0x40) || (0x9c < bVar1)) {
      bVar2 = true;
    }
    else {
      iVar4 = bVar1 + 0x239;
    }
    break;
  case 0x88:
    if ((byte)param_1[1] < 0x9f) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x237;
    }
    break;
  case 0x89:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x2f7;
    }
    break;
  case 0x8a:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x3b7;
    }
    break;
  case 0x8b:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x477;
    }
    break;
  case 0x8c:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x537;
    }
    break;
  case 0x8d:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x5f7;
    }
    break;
  case 0x8e:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x6b7;
    }
    break;
  case 0x8f:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x777;
    }
    break;
  case 0x90:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x837;
    }
    break;
  case 0x91:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x8f7;
    }
    break;
  case 0x92:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0x9b7;
    }
    break;
  case 0x93:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0xa77;
    }
    break;
  case 0x94:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0xb37;
    }
    break;
  case 0x95:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0xbf7;
    }
    break;
  case 0x96:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0xcb7;
    }
    break;
  case 0x97:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0xd77;
    }
    break;
  case 0x98:
    if ((byte)param_1[1] < 0x40) {
      bVar2 = true;
    }
    else {
      iVar4 = (byte)param_1[1] + 0xe37;
    }
  }
  if (!bVar2) {
    puVar3 = &font32_32 + iVar4 * 0x90;
  }
  return puVar3;
}