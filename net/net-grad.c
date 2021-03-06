/* NET-GRAD.C - Routine for calculating gradient from backpropagated info. */

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
#include "prior.h"
#include "model.h"
#include "data.h"
#include "net.h"

/* This module finds the derivatives of the "error" on the training set
   with respect to the network parameters, using the backpropagated 
   derivatives of the error for each training case with respect to the
   unit values. */

/* Added procedures to perform weighted summation of gradient.
 * -- Andrey Popov
 */

static void add_grad1(net_param *, net_value *, int);
static void add_grad2(net_param *, net_value *, net_param *, int,
                      net_value *, int, char *, int);
static void add_grad1_w(net_param *, net_value *, int, double);
static void add_grad2_w(net_param *, net_value *, net_param *, int,
                        net_value *, int, char *, int, double);

/* ADD TO GRADIENT OF ERROR WITH RESPECT TO NETWORK PARAMETERS.  Adds to 
   a set of derivatives with respect to network parameters, stored in a
   structure of the same form as the parameters.  The derivatives added are
   of the "error" for a training case, derived from unit values and 
   derivatives previously computed. 

   One can economize by not bothering to compute the derivatives of the 
   error with respect to the input unit values if the network does not
   have input offset parameters. */

void net_grad(net_params *g,  /* Gradient with respect to parameters to add to */
              net_params *w,  /* Network parameters */
              net_values *v,  /* Values for units in network for a case */
              net_values *d,  /* Backpropagated derivatives for a case */
              net_arch *a,    /* Network architecture */
              net_flags *flgs /* Network flags, null if none */
)
{
  net_grad_w(g, w, v, d, a, flgs, 1.);
}

void net_grad_w(net_params *g,   /* Gradient with respect to parameters to add to */
                net_params *w,   /* Network parameters */
                net_values *v,   /* Values for units in network for a case */
                net_values *d,   /* Backpropagated derivatives for a case */
                net_arch *a,     /* Network architecture */
                net_flags *flgs, /* Network flags, null if none */
                double weight    /* The weight of the current training case */
)
{
  int l;

  if (a->has_ti)
  {
    add_grad1_w(g->ti, d->i, a->N_inputs, weight);
  }

  for (l = 0; l < a->N_layers; l++)
  {
    if (a->has_bh[l])
    {
      add_grad1_w(g->bh[l], d->s[l], a->N_hidden[l], weight);
    }

    if (a->has_ih[l])
    {
      add_grad2_w(g->ih[l], v->i, a->has_ti ? w->ti : 0, a->N_inputs,
                  d->s[l], a->N_hidden[l], flgs ? flgs->omit : 0, 1 << (l + 1), weight);
    }

    if (l > 0 && a->has_hh[l - 1])
    {
      add_grad2_w(g->hh[l - 1], v->h[l - 1], a->has_th[l - 1] ? w->th[l - 1] : 0,
                  a->N_hidden[l - 1], d->s[l], a->N_hidden[l], (char *)0, 0, weight);
    }

    if (a->has_th[l])
    {
      add_grad1_w(g->th[l], d->h[l], a->N_hidden[l], weight);
    }

    if (a->has_ho[l])
    {
      add_grad2_w(g->ho[l], v->h[l], a->has_th[l] ? w->th[l] : 0,
                  a->N_hidden[l], d->o, a->N_outputs, (char *)0, 0, weight);
    }
  }

  if (a->has_io)
  {
    add_grad2_w(g->io, v->i, a->has_ti ? w->ti : 0, a->N_inputs,
                d->o, a->N_outputs, flgs ? flgs->omit : 0, 1, weight);
  }

  if (a->has_bo)
  {
    add_grad1_w(g->bo, d->o, a->N_outputs, weight);
  }
}

/* ADD TO GRADIENT FROM UNIT DERIVATIVE. */

static void add_grad1(net_param *g, /* Array of derivatives to add to */
                      net_value *v, /* Derivatives with respect to unit values */
                      int n         /* Number of units */
)
{
  add_grad1_w(g, v, n, 1.);
}

static void add_grad1_w(net_param *g, /* Array of derivatives to add to */
                        net_value *v, /* Derivatives with respect to unit values */
                        int n,        /* Number of units */
                        double weight /* The weight of the current training case */
)
{
  int i;

  for (i = 0; i < n; i++)
  {
    g[i] += v[i] * weight;
  }
}

/* ADD TO GRADIENT FROM PRODUCT OF UNIT VALUE AND UNIT DERIVATIVE. */

static void add_grad2(net_param *g, /* Array of derivatives to add to */
                      net_value *v, /* Source unit values */
                      net_param *t, /* Offsets for source units, or zero if no offsets */
                      int nv,       /* Number of source units */
                      net_value *d, /* Derivatives with respect to destination units */
                      int nd,       /* Number of destination units */
                      char *omit,   /* Omit flags, null if not present */
                      int b         /* Bit to look at in omit flags */
)
{
  add_grad2_w(g, v, t, nv, d, nd, omit, b, 1.);
}

static void add_grad2_w(net_param *g, /* Array of derivatives to add to */
                        net_value *v, /* Source unit values */
                        net_param *t, /* Offsets for source units, or zero if no offsets */
                        int nv,       /* Number of source units */
                        net_value *d, /* Derivatives with respect to destination units */
                        int nd,       /* Number of destination units */
                        char *omit,   /* Omit flags, null if not present */
                        int b,        /* Bit to look at in omit flags */
                        double weight /* The weight of the current training case */
)
{
  double tv;
  int i, j;

  if (omit == 0)
  {
    if (t != 0)
    {
      for (i = 0; i < nv; i++)
      {
        tv = v[i] + *t++;
        j = 0;
        do
        {
          *g++ += tv * d[j] * weight;
          j += 1;
        } while (j < nd);
      }
    }
    else
    {
      for (i = 0; i < nv; i++)
      {
        tv = v[i];
        j = 0;
        do
        {
          *g++ += tv * d[j] * weight;
          j += 1;
        } while (j < nd);
      }
    }
  }
  else
  {
    if (t != 0)
    {
      for (i = 0; i < nv; i++)
      {
        if ((omit[i] & b) == 0)
        {
          tv = v[i] + *t++;
          j = 0;
          do
          {
            *g++ += tv * d[j] * weight;
            j += 1;
          } while (j < nd);
        }
      }
    }
    else
    {
      for (i = 0; i < nv; i++)
      {
        if ((omit[i] & b) == 0)
        {
          tv = v[i];
          j = 0;
          do
          {
            *g++ += tv * d[j] * weight;
            j += 1;
          } while (j < nd);
        }
      }
    }
  }
}
