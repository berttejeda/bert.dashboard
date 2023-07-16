import base64
import json
import os
import re
import markdown
from btdashboard.config import AppConfig
from btdashboard.defaults import default_verify_tls, default_lessons_config_file
from btdashboard.extensions import NewTabExtension
from jinja2 import Template
from btdashboard.logger import Logger
from btweb import WebAdapter
import urllib.parse

logger = Logger().init_logger(__name__)

class Lessons:

  def __init__(self, **kwargs):

    args = kwargs['args']
    no_render_markdown = args.no_render_markdown
    verify_tls = args.no_verify_tls or default_verify_tls
    lessons_config = AppConfig().initialize(
    args=vars(args),
    config_file=args.lessons_config_file or default_lessons_config_file,
    verify_tls=verify_tls
    )
    self.settings = lessons_config
    fail_on_errors = kwargs.get('fail_on_errors', True)
    self.webadapter = WebAdapter(fail_on_errors=fail_on_errors, verify_tls=verify_tls)
    self.global_username = os.environ.get(
      'GLOBAL_USERNAME') or args.username  # or self.config_util.get(self.settings,'auth.global.username')
    self.global_password = os.environ.get(
      'GLOBAL_PASSWORD') or args.password  # or self.config_util.get(self.settings,'auth.global.password')
    self.slides_pattern = re.compile('^# ')

  def encode_lesson(self, rendered_lesson):
      rendered_lesson_bytes = rendered_lesson.encode("utf-8")
      encoded_lesson = base64.b64encode(rendered_lesson_bytes)
      return encoded_lesson.decode("utf-8")

  def render_lesson(self, lesson_url, lesson_content, no_render_markdown=False):

    initial_data = {
      'environment': os.environ
    }
    lesson_content = str(lesson_content)
    lesson_content = lesson_content.strip()
    lesson_template = Template(lesson_content)
    try:
      rendered_lesson = lesson_template.render(
        session=initial_data
      )
    except Exception as e:
      err = str(e)
      logger.error('I had trouble rendering the lesson at %s, error was %s' % (lesson_url, err))
      rendered_lesson = ('''
        <div class="lesson-error-container">
          <div class="lesson-error-text">
          Error in rendering lesson at %s:<br /> %s
          </div>
        </div>
        ''' % (lesson_url, err)
                         )
      return rendered_lesson
    if no_render_markdown:
      return rendered_lesson
    else:
      rendered_lesson = markdown.markdown(rendered_lesson,
                                          extensions=[NewTabExtension(),
                                                      'markdown.extensions.admonition',
                                                      'markdown.extensions.attr_list',
                                                      'markdown.extensions.codehilite',
                                                      'markdown.extensions.toc',
                                                      'pymdownx.emoji',
                                                      'pymdownx.details']
                                          )
      return rendered_lesson

  def get_markdown_sections(self, content):
    for sec in content.split('\n# '):
      yield sec if sec.startswith('# ') else '# ' + sec

  # TODO: lesson_url should be renamed to lesson_url
  def load_lesson(self, utf8_encoded_uri, no_ui=False, no_render_markdown=False):
    lesson_slug = urllib.parse.unquote(utf8_encoded_uri)
    lesson_slug_parts = lesson_slug.split('/')
    topic_name = lesson_slug_parts[0]
    lesson_name = lesson_slug_parts[-1]
    derived_lesson_obj = [l for l in self.settings.topics[topic_name].lessons if l.get('name') == lesson_name]
    lesson_url = os.environ.get('lesson_url') or derived_lesson_obj[0]['url']
    lesson_type = os.environ.get('lesson_type') or derived_lesson_obj[0].get('type')
    res_ok = False
    # TODO: Employ per-lesson credentials
    if not no_ui:
      try:
        res = self.webadapter.get(lesson_url,
                                  username=self.global_username,
                                  password=self.global_password,
                                  cache_path='.')
        res_ok = True
      except Exception as e:
        err = str(e)
        logger.error('I had trouble retrieving the lesson at %s, error was %s' % (lesson_url, err))
        html_err_message = '''
          <div class="lesson-error-container">
            <div class="lesson-error-text">
            I had trouble retrieving the lesson at %s<br />
            Error was: %s<br />
            </div>
          </div>
        ''' % (lesson_url, err)
        encoded_lesson = self.encode_lesson(html_err_message)
      if res_ok:
        lesson_content = res
        if lesson_type == 'presentation':
          logger.info(f"Lesson at URL {lesson_url} is of type 'presentation', not rendering HTML")
          lesson_content_obj = [sec for i,sec in enumerate(self.get_markdown_sections(lesson_content))]
          lesson_content_output = json.dumps(lesson_content_obj)
          logger.debug(lesson_content)
        else:
          logger.info('Attempting to render and encode lesson at %s' % lesson_url)
          lesson_content_output = self.render_lesson(lesson_url, lesson_content, no_render_markdown=no_render_markdown)
          logger.debug(lesson_content_output)
        try:
          encoded_lesson = self.encode_lesson(lesson_content_output)
        except Exception as e:
          err = str(e)
          logger.error('I had trouble encoding the lesson at %s' % lesson_url, err)
          html_err_message = '''
            <div class="lesson-error-container">
              <div class="lesson-error-text">
              I had trouble encoding the lesson at %s<br />
              Error was: %s
              </div>
            </div>
          ''' % (lesson_url, err)
          encoded_lesson = self.encode_lesson(html_err_message)
      encoded_lesson_obj = {'encodedLesson': encoded_lesson }
      return(encoded_lesson_obj)
    else:
      res = self.webadapter.get(lesson_url,
                                username=self.global_username,
                                password=self.global_password,
                                cache_path='.')
      lesson_content = str(res)
      lesson_content_output = self.render_lesson(lesson_content, no_render_markdown=no_render_markdown)
      print(lesson_content_output)

  def save_content(self, content):
    filename = self.webview.windows[0].create_file_dialog(self.webview.SAVE_DIALOG)
    if not filename:
      return

    with open(filename, 'w') as f:
      f.write(content)