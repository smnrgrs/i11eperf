/*
 * Copyright(c) 2021 ADLINK Technology Limited and others
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0, or the Eclipse Distribution License
 * v. 1.0 which is available at
 * http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * SPDX-License-Identifier: EPL-2.0 OR BSD-3-Clause
 */
#include <cstdlib>
#include <csignal>
#include <iostream>
#include <chrono>
#include <thread>

#include "dds/dds.hpp"
#include "i11eperf.hpp"
#include "config.h"

#include "dds/dds.h"
static void batching()
{
#if BATCHING
  dds_write_set_batch (true);
#endif
}

static volatile sig_atomic_t interrupted = 0;
static void sigh (int sig __attribute__ ((unused))) { interrupted = 1; }

template<typename T>
static void pub(dds::domain::DomainParticipant& dp)
{
  dds::topic::Topic<T> tp(dp, "Data");
  dds::pub::Publisher pub(dp);
  dds::pub::qos::DataWriterQos qos;
  qos << dds::core::policy::Reliability::Reliable(dds::core::Duration::infinite())
      << dds::core::policy::History::HISTORY_KIND;
  batching();
  dds::pub::DataWriter<T> wr(pub, tp, qos);

  signal(SIGTERM, sigh);
  T sample{};
  while (!interrupted)
  {
    wr << sample;
    ++sample.s();
#if SLEEP_MS != 0
    dds_write_flush(wr->get_ddsc_entity()); // so we can forget about BATCHING
    std::this_thread::sleep_for(std::chrono::milliseconds(SLEEP_MS));
#endif
  }
}

int main()
{
  dds::domain::DomainParticipant dp(0);
  pub<DATATYPE_CPP>(dp);
  return 0;
}
