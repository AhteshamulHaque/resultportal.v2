# import command related arguments and options to pass to the main app
from .config import register_config_parser, execute_config_cmd
from .student import register_student_parser, execute_student_cmd
from .log import register_log_parser, execute_log_cmd
from .image import register_image_parser, execute_image_cmd
from .pdf import register_pdf_parser, execute_pdf_cmd
from .rank import register_rank_parser, execute_rank_cmd
from .scraper import register_scraper_parser, execute_scrape_cmd
from .verify import register_verify_parser, execute_verify_cmd
