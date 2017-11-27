from django.utils.safestring import mark_safe


class Page:
    def __init__(self, current_page, data_count, per_page_count=4, pager_num=7):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num

    @property   #可以直接调用不用加()，好看一些
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
            prev = '<li><a class="page" href="javascript:void(0);">&laquo;</a></li>'
        else:
            prev = '<li><a class="page" href="%s?p=%s">&laquo;</a></li>' % (base_url, self.current_page - 1,)
        page_list.append(prev)

        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                temp = '<li><a class="page active" href="%s?p=%s">%s</a></li>' % (base_url, i, i)
            else:
                temp = '<li><a class="page" href="%s?p=%s">%s</a></li>' % (base_url, i, i)
            page_list.append(temp)

        if self.current_page == self.total_count:
            nex = '<li><a class="page" href="javascript:void(0);">&raquo;</a></li>'
        else:
            nex = '<li><a class="page" href="%s?p=%s">&raquo;</a></li>' % (base_url, self.current_page + 1,)
        page_list.append(nex)

        # jump = """
        # <input type='text'  /><a onclick='jumpTo(this, "%s?p=");'>GO</a>
        # <script>
        #     function jumpTo(ths,base){
        #         var val = ths.previousSibling.value;
        #         location.href = base + val;
        #     }
        # </script>
        # """ % (base_url,)

        # page_list.append(jump)
        if self.data_count/self.per_page_count > 1:
            page_str = mark_safe("".join(page_list))
        else:
            page_str = ''
        return page_str

