import cocos

from game.visualizer.load import load


class LoadingLayer(cocos.layer.Layer):
    def __init__(self, assets, post_method):
        super().__init__()

        self.assets = assets
        self.post_method = post_method

        self.loading_order = {
            1: "Loading city assets",
            2: "Loading side structures",
            3: "Creating disasters",
            4: "Initializing forecasts",
            5: "Constructing sensors",
            6: "Writing decrees",
            7: "Importing workers",
            8: "Cleaning up"
        }

        self.label = cocos.text.Label(
            '',
            font_name='Arial',
            font_size=16,
            color=(255, 255, 255, 255),
            anchor_x='center',
            anchor_y='center'

        )
        self.label.position = 640, 360
        self.add(self.label)

        self.bar = cocos.draw.Line(
            (540, 260),
            (540, 260),
            color=(0, 150, 255, 255),
            stroke_width=16
        )
        self.add(self.bar)

        self.current_key = 0
        self.schedule_interval(callback=self.load_assets, interval=0.5)

    def load_assets(self, interval):
        self.current_key += 1

        if self.current_key in self.loading_order:
            item = self.loading_order[self.current_key]

            self.label.element.text = item
            self.bar.end = (540 + (200 * self.current_key / len(self.loading_order)), 260)

            load(self.assets, self.current_key)
        else:
            self.post_method()
