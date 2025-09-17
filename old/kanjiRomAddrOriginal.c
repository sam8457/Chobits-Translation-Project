
undefined * kanjiRomAdrOriginal(undefined1 *char_code)

{
  byte second_byte;
  bool doesnt_exist;
  undefined *char_offset;
  int char_index;
  
  char_offset = (undefined *)0x0;
  char_index = 0;
  doesnt_exist = false;
  switch(*char_code) {
  case 0x81:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte - 0x40;
    }
    break;
  case 0x82:
    second_byte = char_code[1];
    if ((second_byte < 0x4f) || (0xf1 < second_byte)) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x71;
    }
    break;
  case 0x83:
    second_byte = char_code[1];
    if ((second_byte < 0x40) || (0xd6 < second_byte)) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x123;
    }
    break;
  case 0x84:
    second_byte = char_code[1];
    if ((second_byte < 0x40) || (0xbe < second_byte)) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x1ba;
    }
    break;
  default:
    doesnt_exist = true;
    break;
  case 0x87:
    second_byte = char_code[1];
    if ((second_byte < 0x40) || (0x9c < second_byte)) { 
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x239;
    }
    break;
  case 0x88:
    if (second_byte < 0x9f) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x237;
    }
    break;
  case 0x89:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x2f7;
    }
    break;
  case 0x8a:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x3b7;
    }
    break;
  case 0x8b:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x477;
    }
    break;
  case 0x8c:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x537;
    }
    break;
  case 0x8d:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x5f7;
    }
    break;
  case 0x8e:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x6b7;
    }
    break;
  case 0x8f:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x777;
    }
    break;
  case 0x90:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x837;
    }
    break;
  case 0x91:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x8f7;
    }
    break;
  case 0x92:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0x9b7;
    }
    break;
  case 0x93:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0xa77;
    }
    break;
  case 0x94:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0xb37;
    }
    break;
  case 0x95:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0xbf7;
    }
    break;
  case 0x96:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0xcb7;
    }
    break;
  case 0x97:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0xd77;
    }
    break;
  case 0x98:
    if (second_byte < 0x40) {
      doesnt_exist = true;
    }
    else {
      char_index = second_byte + 0xe37;
    }
  }
  if (! doesnt_exist) {
    char_offset = font_offset_start + char_index * 144; 
  }
  return char_offset;
}