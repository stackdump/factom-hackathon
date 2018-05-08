""" main app entrypoint """
import terminal

def main(cfg, ctx):
    ctx.bind(schema='octoe', callback=ctx.on_event)

terminal.__onload(callback=main)
