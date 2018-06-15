# Pet Registry Index

Submission for Factom Blockchain hackathon - We were awarded 1st place & $5k!!

https://www.factom.com/blog/factom-blockchain-vs-paper-hackathon-june-9-10-in-austin

## Summary

App published streams of 'pet' and 'vet' events to factom's blockchain - securing the USDA travel certification process to make it impossible to forge this form: https://www.aphis.usda.gov/library/forms/pdf/APHIS7001.pdf …  Ideal is to prevent spread of Zoonotic diseases like rabies to biosecure regions like Hawaii

## Links

Video of all presentations https://t.co/0fuQLEcmdk

Team Zoo Slides: https://github.com/stackdump/factom-hackathon/blob/master/ZooRegistryIndex.pdf

Learn more about this design for event-sourced applications on the blog: https://www.blahchain.com/

## What's different about this?

Because Factom allows you to attach arbitrary data to the blockchain--
We are able to create an immutable stream of 'pet' and 'vet' event data.

Using the Petri-Net notation allows us to publish the event schema as 'just' another event.

The overall effect of this approach is that the continuous stream is both immutable and updatable.

This pattern is known as 'Event Souring' https://martinfowler.com/eaaDev/EventSourcing.html
