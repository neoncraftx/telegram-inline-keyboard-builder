export class TelebotInlineAdapter {
  createCallback(text, data) {
    return { text, callback: data };
  }
  createUrl(text, url) {
    return { text, url };
  }
  createPay(text) {
    return { text, pay: true };
  }
  buildKeyboard(rows) {
    return Telebot.inlineKeyboard(rows);
  }
}