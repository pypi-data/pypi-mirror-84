import logging

class DiscordReportFormatter(logging.Formatter):
  """
  A log formatter specializing in sending logs to Discord.
  Specifically, use Markdown emphasis format in various parts of the log to make the log easier to read.
  """
  LEVELNAME2EMOJI = {
    "DEBUG": ":detective: ",
    "INFO": ":speech_balloon: ",
    "WARNING": ":warning: ",
    "ERROR": ":exclamation: ",
    "CRITICAL": ":bangbang: ",
  }

  def format(self, record):
    """
    The only override method.
    Format items such as the first line.
    """
    record.message = record.getMessage()
    if self.usesTime():
      record.asctime = self.formatTime(record, self.datefmt)
    l = self.formatMessage(record).splitlines()
    l[0] = f"**{l[0]}**"
    s = ""
    if record.levelname in self.LEVELNAME2EMOJI:
      s = self.LEVELNAME2EMOJI[record.levelname]
    s += "\n".join(l)
    if record.exc_info:
      # Cache the traceback text to avoid converting it multiple times
      # (it's constant anyway)
      if not record.exc_text:
        record.exc_text = self.formatException(record.exc_info)
    if record.exc_text:
      if s[-1:] != "\n":
        s = s + "\n"
      s = "{0}**exc**\n```\n{1}\n```".format(s, record.exc_text)
    if record.stack_info:
      if s[-1:] != "\n":
        s = s + "\n"
      s = "{0}**stack**\n```\n{1}\n```".format(s, self.formatStack(record.stack_info))
    return s
