/*
Copyright (C) 2015- The University of Notre Dame
This software is distributed under the GNU General Public License.
See the file COPYING for details.
*/

#ifndef JX_PRINT_H
#define JX_PRINT_H

/** @file jx_print.h Print JX expressions to strings, files, and buffers. */

#include "jx.h"
#include "buffer.h"
#include "link.h"
#include <stdio.h>

/** Convert a JX expression into a string.  @param j A JX expression. @return A C string representing the expression in JSON form.  The string must be deleted with free(). */

char * jx_print_string( struct jx *j );

/** Print a JX expression to a standard I/O stream.  @param j A JX expression.  @param file A standard IO stream. */

void jx_print_stream( struct jx *j, FILE *file );

/** Print a JX expression to a buffer. @param j A JX expression. @param buffer The buffer for output. @see buffer.h */

void jx_print_buffer( struct jx *j, buffer_t *buffer);

/** Print a JX expression to a link. @param j A JX expression. @param l The network link to write. @param stoptime The absolute time to stop. @see link.h */

void jx_print_link( struct jx *j, struct link *l, time_t stoptime );

/** Print a C string in JSON format (with escape codes) into a buffer.  @param s A C string.  @param b The buffer for output.  @see buffer.h */
void jx_escape_string( const char *s, buffer_t *b );

#endif
