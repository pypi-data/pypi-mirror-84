from contextlib import contextmanager
import justpy as jp


@contextmanager
def _(w):
    # to nest gui building
    yield w


class DefaultLayout(jp.QuasarPage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = jp.QLayout(view="hHh Lpr lff", classes="q-pa-md", style="height:300px", a=self)

        async def toggle_menu(comp, msg):
            print("button clicked")
            await drawer.run_method("toggle()", msg.websocket)

        with _(jp.QHeader(elevated=True, classes="bg-black", a=layout)) as header:
            with _(jp.QToolbar(a=header)) as toolbar:
                toolbar += jp.QBtn(flat=True, round=True, dense=True, icon="menu", click=toggle_menu)
                toolbar += jp.QToolbarTitle(text="Header!!")

        with _(
            jp.QDrawer(
                v_model="drawer",
                show_if_above=True,
                width=200,
                breakpoint=500,
                bordered=True,
                content_class="bg-grey-3",
                a=layout,
            )
        ) as drawer:
            with _(jp.QScrollArea(classes="fit", a=drawer)) as scrollarea:
                with _(jp.QList(a=scrollarea)) as qlist:
                    with _(jp.Div(a=qlist)) as menu:
                        self.menu = menu
        page_container = jp.QPageContainer(a=layout)
        self.content = jp.QPage(padding=True, a=page_container)



def main():
    """ Usage """

    def create_wp():
        """Create separate websession

        Otherwise, it's a shared session which of course can be cool.
        """
        wp = DefaultLayout()  # delete_flag=False)
        return wp

    def foo(self, msg):
        msg.page.content.delete_components()
        jp.QBtn(text="back to main", click=index, a=msg.page.content)
        for n in range(0, 155):
            msg.page.content.add(
                jp.P(
                    text="Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?"
                )
            )

    def index(self, msg):
        msg.page.content.delete_components()
        jp.QBtn(text="foo", click=foo, a=msg.page.content)

    def create_menu(menu_list, wp3):
        wp3.menu.delete_components()
        for i, menu in enumerate(menu_list):
            qitem = jp.QItem(clickable=True, v_ripple=True, a=wp3.menu, click=menu["page"])
            qs1 = jp.QItemSection(avatar=True, a=qitem)
            qs1 += jp.QIcon(name=menu["icon"])
            qitem += jp.QItemSection(text=menu["label"])
            if menu["separator"]:
                wp3.menu += jp.QSeparator(key="sep" + str(i))

    def app():

        wp = create_wp()  # if you want separate web sessions
        menu_list = [
            {"icon": "inbox", "label": "Inbox", "separator": True, "page": foo},
            {"icon": "send", "label": "Outbox", "separator": False, "page": index},
            {"icon": "delete", "label": "Trash", "separator": False, "page": foo},
            {"icon": "error", "label": "Spam", "separator": True, "page": index},
            {
                "icon": "settings",
                "label": "Settings",
                "separator": False,
                "page": foo,
            },
            {
                "icon": "feedback",
                "label": "Send Feedback",
                "separator": False,
                "page": index,
            },
            {
                "icon": "help",
                "iconColor": "primary",
                "label": "Help",
                "separator": False,
                "page": foo,
            },
        ]
        create_menu(menu_list, wp)

        class msg(object):  # a weird bit since we're avoiding use of requests
            page = wp

        index(None, msg)
        return wp

    jp.justpy(app)
    # japp = jp.app
    # jp.justpy(app, start_server=False)
    # from starlette.testclient import TestClient
    # from starlette.testclient import TestClient

    # def test_app():
    #     client = TestClient(japp)
    #     response = client.get("/")
    #     assert response.status_code == 200
    #     print(response.status_code)
    #     import pdb

    #     pdb.set_trace()

    # test_app()

if __name__ == "__main__":
    main()