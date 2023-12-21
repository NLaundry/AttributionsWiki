-- CreateTable
CREATE TABLE "_BeliefAttribution" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "_BeliefAttribution_AB_unique" ON "_BeliefAttribution"("A", "B");

-- CreateIndex
CREATE INDEX "_BeliefAttribution_B_index" ON "_BeliefAttribution"("B");

-- AddForeignKey
ALTER TABLE "_BeliefAttribution" ADD CONSTRAINT "_BeliefAttribution_A_fkey" FOREIGN KEY ("A") REFERENCES "Attribution"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_BeliefAttribution" ADD CONSTRAINT "_BeliefAttribution_B_fkey" FOREIGN KEY ("B") REFERENCES "Belief"("id") ON DELETE CASCADE ON UPDATE CASCADE;
