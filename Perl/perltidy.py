import sublime, sublime_plugin
import subprocess, os.path

class PerlTidyCommand(sublime_plugin.TextCommand):
	"""
	Use this command to pretty print Perl code.

	It pretty-prints the selected region or the entire file.

	Will use the installed PerlTidy if found, else will use the embedded
	PerlTidy in which case a Perl interpreter must be in the PATH environment variable

	See http://perltidy.sourceforge.net/ for more information
	"""

	# Default path to PerlTidy, change this to your own PerlTidy installation if you have one
	DefaultPerlTidy = '/usr/bin/perltidy'

	# Pretty printing parameters, customize to your liking
	PrettyPrintingParams = [
		"-sbl",     # open sub braces on new line
		"-bbt=1",   # add only some spaces in single-line curly braces
		"-pt=2",    # dont add spaces inside parenthesis
		"-nbbc",    # don't add blank lines before comments
		"-l=80",    # wrap at column 100
		"-ole=unix" # unix line endings
	]

	def run(self, edit):
		if self.view.sel()[0].empty():
			# nothing selected: process the entire file
			r = sublime.Region(0L, self.view.size())
		else:
			# process only selected region
			r = self.view.line(self.view.sel()[0])

		# Run PerlTidy, and restore approximate cursor location
		cursor = self.view.sel()[0];
		self.tidyRegion(r)
		if cursor.empty():
			self.view.sel().add(cursor)
			self.view.sel().subtract(self.view.sel()[1])

	def tidyRegion(self, region):
		if os.path.isfile(self.DefaultPerlTidy):
			# use installed PerlTidy
			cmd = [self.DefaultPerlTidy]
			# print "using installed PerlTidy", cmd
		else:
			# use packaged PerlTidy, needs Perl to run
			cmd = ["perl", sublime.packages_path() + "/Perl/perltidy"]
			# print "using packaged PerlTidy", cmd

		cmd += [
			"-w", # report all errors and warnings
			"-se" # send error message to stderr rather than filename.err
		]

		cmd += self.PrettyPrintingParams # add pretty printing parameters

		p = subprocess.Popen(
			cmd,
			shell   = True,
			bufsize = -1,
			stdout  = subprocess.PIPE,
			stderr  = subprocess.PIPE,
			stdin   = subprocess.PIPE)

		output, error = p.communicate(self.view.substr(region))
		e = self.view.begin_edit()
		self.view.replace(e,region, output)
		self.view.end_edit(e)

		if error:
			results = self.view.window().new_file()
			results.set_scratch(results.buffer_id())
			results.set_name("PerlTidy error output")
			results.insert(0, error)

	def isEnabled(self, args):
		# enabled for Perl and Plain text files, with at most 1 selection region
		return len(self.view.sel()) == 1 and self.view.settings().get("syntax") in [u"Packages/Perl/Perl.tmLanguage", u"Packages/Text/Plain text.tmLanguage"]
