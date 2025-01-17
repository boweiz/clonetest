from scrapy import log
from scrapy.http import Request

class DepthMiddleware(object):

    def __init__(self, maxdepth, stats=None, verbose_stats=False, prio=1):
        self.maxdepth = maxdepth
        self.stats = stats
        self.verbose_stats = verbose_stats
        self.prio = prio

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        maxdepth = settings.getint('DEPTH_LIMIT')
        verbose = settings.getbool('DEPTH_STATS_VERBOSE')
        prio = settings.getint('DEPTH_PRIORITY')
        return cls(maxdepth, crawler.stats, verbose, prio)

    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request):
                inc = not request.meta.get('dont_increase_depth', False)
                depth = response.meta['depth'] + (1 if inc else 0)
                request.meta['depth'] = depth
                if self.prio and inc:
                    request.priority -= depth * self.prio
                if self.maxdepth and depth > self.maxdepth:
                    log.msg(format="Ignoring link (depth > %(maxdepth)d): %(requrl)s ",
                            level=log.DEBUG, spider=spider,
                            maxdepth=self.maxdepth, requrl=request.url)
                    return False
                elif self.stats:
                    if self.verbose_stats:
                        self.stats.inc_value('request_depth_count/%s' % depth, spider=spider)
                    self.stats.max_value('request_depth_max', depth, spider=spider)
            return True

        # base case (depth=0)
        if self.stats and 'depth' not in response.meta:
            response.meta['depth'] = 0
            if self.verbose_stats:
                self.stats.inc_value('request_depth_count/0', spider=spider)

        return (r for r in result or () if _filter(r))