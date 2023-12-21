/*
  Warnings:

  - A unique constraint covering the columns `[attributionId]` on the table `Factor` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[beliefId]` on the table `Factor` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "Factor" ADD COLUMN     "attributionId" INTEGER,
ADD COLUMN     "beliefId" INTEGER;

-- CreateIndex
CREATE UNIQUE INDEX "Factor_attributionId_key" ON "Factor"("attributionId");

-- CreateIndex
CREATE UNIQUE INDEX "Factor_beliefId_key" ON "Factor"("beliefId");

-- AddForeignKey
ALTER TABLE "Factor" ADD CONSTRAINT "Factor_attributionId_fkey" FOREIGN KEY ("attributionId") REFERENCES "Attribution"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Factor" ADD CONSTRAINT "Factor_beliefId_fkey" FOREIGN KEY ("beliefId") REFERENCES "Belief"("id") ON DELETE SET NULL ON UPDATE CASCADE;
