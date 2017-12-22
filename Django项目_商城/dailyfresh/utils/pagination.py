from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, current_page,nid,tid,data_count, per_page_count=10, pager_num=7):
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num
        self.nid = nid
        self.tid = tid

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    @property
    def total_count(self):
        v, y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v

    def page_str(self, base_url):
        page_list = []

        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1

        if self.current_page == 1:
            prev = '<a href="javascript:void(0);">上一页</a>'
        else:
            prev = '<a class="page" href="%s%s-%s-%s.html">上一页</a>' % (base_url,self.nid,self.tid,self.current_page - 1,)
        page_list.append(prev)

        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                temp = '<a class="active" href="%s%s-%s-%s.html">%s</a>' % (base_url,self.nid,self.tid, i, i)
            else:
                temp = '<a href="%s%s-%s-%s.html">%s</a>' % (base_url,self.nid,self.tid, i, i)
            page_list.append(temp)

        if self.current_page == self.total_count:
            nex = '<a href="javascript:void(0);">下一页</a>'
        else:
            nex = '<a href="%s%s-%s-%s.html">下一页</a>' % (base_url,self.nid,self.tid, self.current_page + 1,)
        page_list.append(nex)

        if self.data_count / self.per_page_count > 1:
            page_str = mark_safe("".join(page_list))
        else:
            page_str = ''

        return page_str