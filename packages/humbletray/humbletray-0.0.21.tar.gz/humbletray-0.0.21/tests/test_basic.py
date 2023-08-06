import justpy as jp


def test_imports():
    from humbletray import main, systray

def test_leaf_icon():
    from humbletray import systray
    fig = systray.fig_full_path
    assert 'leaf.png' in fig

def test_quasar_layout():
    from humbletray import layout
    """Basic sanity checks."""
    default = layout.DefaultLayout()
    default.content.add(jp.Div(text="success"))
    assert 'success' in default.to_html()
    assert 'q-layout' in default.to_html()

