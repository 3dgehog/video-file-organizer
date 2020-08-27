from video_file_organizer.rules import series
from video_file_organizer.rules.utils import RuleRegistry

RuleRegistry.add_rule('season', series.rule_season,
                      'OutputFolderMatcher/after', 10)

RuleRegistry.add_rule('parent-dir', series.rule_parent_dir,
                      'OutputFolderMatcher/after', 10)

RuleRegistry.add_rule('sub-dir', series.rule_sub_dir,
                      'OutputFolderMatcher/after', 10)

RuleRegistry.add_rule('episode-only', series.rule_episode_only,
                      'OutputFolderMatcher/after', 20)

RuleRegistry.add_rule('format-title', series.rule_format_title,
                      'OutputFolderMatcher/after', 20)

RuleRegistry.add_rule('alt-title', series.rule_alt_title,
                      'RuleBookMatcher/after', 20)
