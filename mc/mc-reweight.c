/* MC-REWEIGHT.C - Copy part of a log file while changing iteration weights. */

/* Copyright (c) 1995-2004 by Radford M. Neal 
 *
 * Permission is granted for anyone to copy, use, modify, or distribute this
 * program and accompanying programs and documents for any purpose, provided 
 * this copyright notice is retained and prominently displayed, along with
 * a note saying that the original programs are available from Radford Neal's
 * web page, and note is made of any changes made to the programs.  The
 * programs and documents are distributed without any warranty, express or
 * implied.  As the programs were written for research purposes only, they have
 * not been tested to the degree that would be advisable in any important
 * application.  All use of these programs is entirely at the user's own risk.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

#include "misc.h"
#include "log.h"
#include "mc.h"

static void usage(void);

/* MAIN PROGRAM. */

main(int argc,
     char **argv)
{
  log_file logf_in, logf_out;
  int low, high, modulus;
  int lasti, lasto;
  mc_iter *it;
  void *data;
  float w;

  if (argc != 4)
    usage();

  logf_in.file_name = argv[1];
  log_file_open(&logf_in, 0);

  parse_range(argv[2], &low, &high, &modulus);
  if (modulus < 0)
  {
    fprintf(stderr, "Bad range specification: %s\n", argv[2]);
    exit(1);
  }
  if (high == -2)
    high = low;

  logf_out.file_name = argv[3];
  log_file_create(&logf_out);

  lasti = -1;
  lasto = -1;

  while (!logf_in.at_end && (high < 0 || logf_in.header.index <= high))
  {
    data = 0;

    if (logf_in.header.index < 0 || logf_in.header.index >= low && logf_in.header.index % modulus == 0)
    {
      data = malloc(logf_in.header.size);
      if (data == 0)
      {
        fprintf(stderr, "Not enough memory for record of size %d - ignored\n",
                logf_in.header.size);
      }
    }

    if (data == 0)
    {
      log_file_forward(&logf_in);
      continue;
    }

    logf_out.header = logf_in.header;
    log_file_read(&logf_in, data, logf_in.header.size);

    if (logf_out.header.type == 'i')
    {
      if (logf_out.header.size != sizeof(mc_iter))
      {
        fprintf(stderr, "MC iteration record is the wrong size! (%d %d)\n",
                logf_in.header.size, sizeof(mc_iter));
        exit(1);
      }
      it = (mc_iter *)data;
      if (scanf("%f", &w) != 1)
      {
        fprintf(stderr, "Error reading log weight from standard input\n");
        exit(1);
      }

      it->log_weight += w;
    }

    log_file_append(&logf_out, data);

    free(data);
  }

  log_file_close(&logf_in);
  log_file_close(&logf_out);

  exit(0);
}

/* PRINT USAGE MESSAGE AND EXIT. */

void usage(void)
{
  fprintf(stderr,
          "Usage: mc-reweight logfile-in range logfile-out < file-of-log-weights\n");
  exit(1);
}
