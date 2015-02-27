class ClassImporter(object):

	# because python does not support circular imports

	@staticmethod
	def importAllClasses():
		import classes
		import classes.Clipboard
		import classes.Config
		import classes.Constants
		import classes.Fp
		import classes.Pointer
		import classes.TimerHandler

		import classes.Drawable
		import classes.Drawable.AbstractDrawable
		import classes.Drawable.AbstractEventHandler

		import classes.Drawable.Screen
		import classes.Drawable.Screen.Screen
		import classes.Drawable.Screen.FocusedScreenEventHandler

		import classes.Drawable.Screen.Block
		import classes.Drawable.Screen.Block.AbstractBlock
		import classes.Drawable.Screen.Block.TextBlock
		import classes.Drawable.Screen.Block.ImageBlock
		import classes.Drawable.Screen.Block.FocusedTextBlockEventHandler

		import classes.Drawable.Screen.Block.Textfield
		import classes.Drawable.Screen.Block.Textfield.AbstractTextfield
		import classes.Drawable.Screen.Block.Textfield.Textfield
		import classes.Drawable.Screen.Block.Textfield.FocusedInputEventHandler

		import classes.Drawable.Screen.Block.Textfield.Paragraph
		import classes.Drawable.Screen.Block.Textfield.Paragraph.Paragraph
		import classes.Drawable.Screen.Block.Textfield.Paragraph.FocusedParagraphEventHandler

		# import classes.Drawable.Screen.Block.Textfield.Paragraph.TextLine

